from typing import Callable, Dict

import pandas as pd

from py_replay_bg.environment import Environment
from py_replay_bg.model.t1d_model_single_meal import T1DModelSingleMeal
from py_replay_bg.model.t1d_model_multi_meal import T1DModelMultiMeal

from py_replay_bg.dss import DSS
from py_replay_bg.dss.default_dss_handlers import default_meal_generator_handler, standard_bolus_calculator_handler, \
    default_basal_handler, ada_hypotreatments_handler, corrects_above_250_handler

from py_replay_bg.data import ReplayBGData

from py_replay_bg.identification.mcmc import MCMC
from py_replay_bg.identification.map import MAP
from py_replay_bg.replay import Replayer
from py_replay_bg.visualizer import Visualizer

from py_replay_bg.input_validation import InputValidator

import os

import pickle

from py_agata.py_agata import Agata
from py_agata.utils import glucose_vector_to_dataframe
from py_agata.error import *


class ReplayBG:
    """
    Core class of ReplayBG
    
    ...
    Attributes 
    ----------
    environment: Environment
        An object that represents the hyperparameters to be used by ReplayBG environment.
    model: Model
        An object that represents the physiological model to be used by ReplayBG.
    identifier: MCMC | MAP
        An object that represents the hyperparameters of the object that orchestrates the identification procedure.
    dss: DSS
        An object that represents the hyperparameters of the integrated decision support system.

    Methods
    -------
    run():
        Runs ReplayBG.
    """

    def __init__(self, modality: str, data: pd.DataFrame, bw: float, scenario: str, save_name: str, save_folder: str,
                 u2ss: float | None = None, X0: np.ndarray | None = None, previous_data_name: str | None  = None,

                 identification_method: str = 'mcmc',

                 yts: int = 5, glucose_model: str = 'IG', pathology: str = 't1d', exercise: bool = False, seed: int = 1,

                 bolus_source: str = 'data', basal_source: str = 'data', cho_source: str = 'data', cgm_model: str = 'CGM',

                 n_steps: int = 10000, save_chains: bool = False, analyze_results: bool = True,

                 CR: float = 10, CF: float = 40, GT: float = 120,
                 meal_generator_handler: Callable = default_meal_generator_handler, meal_generator_handler_params: Dict = {},
                 bolus_calculator_handler: Callable = standard_bolus_calculator_handler, bolus_calculator_handler_params: Dict = {},
                 basal_handler: Callable = default_basal_handler, basal_handler_params: Dict = {},
                 enable_hypotreatments: bool = False, hypotreatments_handler: Callable = ada_hypotreatments_handler, hypotreatments_handler_params: Dict = {},
                 enable_correction_boluses: bool = False, correction_boluses_handler: Callable = corrects_above_250_handler, correction_boluses_handler_params: Dict = {},

                 save_suffix: str = '',
                 save_workspace: bool = False,
                 parallelize: bool = False, n_processes: int | None = None,

                 plot_mode: bool = True, verbose: bool = True):
        """
        Constructs all the necessary attributes for the ReplayBG object.

        Parameters
        ----------
        modality : str, {'identification', 'replay'}
            A string that specifies if the function will be used to identify 
            the ReplayBG model on the given data or to replay the scenario specified by 
            the given data.
        data: pd.DataFrame
            Pandas dataframe which contains the data to be used by the tool.
        bw: float
            The patient's body weight.
        scenario: str, {'single-meal', 'multi-meal'}
            A string that specifies whether the given scenario refers to a single-meal scenario or a multi-meal scenario.
        save_name : str
            A string used to label, thus identify, each output file and result.
        save_folder : str
            A string defining the folder that will contain the results.

        u2ss : float, optional, default : None
            The steady state of the basal insulin infusion.
        X0 : np.ndarray, optional, default : None
            The initial model conditions.
        previous_data_name : str, optional, default : None
            The name of the previous data portion. This is used to correcly "trasfer" the initial model conditions to
            the current portion of data.

        identification_method : str, {'mcmc', 'map'}, optional, default : 'mcmc'
            The method to be used to identify the model.

        yts: int, optional, default : 5
            An integer that specifies the data sample time (in minutes).
        glucose_model: str, {'IG','BG'}
            The model equation to be used as measured glucose.
        pathology: str, {'t1d', 't2d', 'pbh', 'healthy'}, optional, default: 't1d'
            A string that specifies the patient pathology.
        exercise: boolean, optional, default : False
            A boolean that specifies whether to simulate exercise or not.
        seed: int, optional, default: 1
            An integer that specifies the random seed. For reproducibility.

        bolus_source : str, {'data', or 'dss'}, optional, default : 'data'
            A string defining whether to use, during replay, the insulin bolus data contained in the 'data' timetable (if 'data'),
            or the boluses generated by the bolus calculator implemented via the provided 'bolusCalculatorHandler' function.
        basal_source : str, {'data', 'u2ss', or 'dss'}, optional, default : 'data'
            A string defining whether to use, during replay, the insulin basal data contained in the 'data' timetable (if 'data'), 
            or the basal generated by the controller implemented via the provided 'basalControllerHandler' function (if 'dss'), 
            or fixed to the average basal rate used during identification (if 'u2ss').
        cho_source : str, {'data', 'generated'}, optional, default : 'data'
            A string defining whether to use, during replay, the CHO data contained in the 'data' timetable (if 'data'),
            or the CHO generated by the meal generator implemented via the provided 'mealGeneratorHandler' function.
        cgm_model: str, {'CGM','IG'}, optional, default : 'CGM'
            A string that specify the cgm model selection.
            If IG is selected, CGM measure will be the noise-free IG state at the current time.

        n_steps: int, optional, default : 10000
            Number of steps to use for the main chain. This is ignored if modality is 'replay'.
        save_chains: bool, optional, default : False
            A flag that specifies whether to save the resulting mcmc chains and copula samplers.
        analyze_results : bool, optional, default : True
            A flag that specifies whether to analyze the resulting trace or not. Setting this flag to False will fasten
            ReplayBG and it is recommended if ReplayBG will be a component of a bigger framework (e.g., to be used in an
            iterative process).

        CR: float, optional, default : 10
            The carbohydrate-to-insulin ratio of the patient in g/U to be used by the integrated decision support system.
        CF: float, optional, default : 40
            The correction factor of the patient in mg/dl/U to be used by the integrated decision support system.
        GT: float, optional, default : 120
            The target glucose value in mg/dl to be used by the decsion support system modules.
        meal_generator_handler: function, optional, default : default_meal_generator_handler
            A callback function that implements a meal generator to be used during the replay of a given scenario.
        meal_generator_handler_params: dict, optional, default : {}
            A dictionary that contains the parameters to pass to the meal_generator_handler function.
        bolus_calculator_handler: function, optional, default : standard_bolus_calculator_handler
            A callback function that implements a bolus calculator to be used during the replay of a given scenario.
        bolus_calculator_handler_params: dict, optional, default : {}
            A dictionary that contains the parameters to pass to the bolusCalculatorHandler function. It also serves as memory
            area for the bolusCalculatorHandler function.
        basal_handler: function, optional, default : default_basal_handler
            A callback function that implements a basal controller to be used during the replay of a given scenario.
        basal_handler_params: dict, optional, default : {}
            A dictionary that contains the parameters to pass to the basalHandler function. It also serves as memory area for the basalHandler function.
        enable_hypotreatments: boolean, optional, default : False
            A flag that specifies whether to enable hypotreatments during the replay of a given scenario.
        hypotreatments_handler: function, optional, default : ada_hypotreatments_handler
            A callback function that implements an hypotreatment strategy during the replay of a given scenario.
        hypotreatments_handler_params: dict, optional, default : {}
            A dictionary that contains the parameters to pass to the hypoTreatmentsHandler function. It also serves as memory
            area for the hypoTreatmentsHandler function.
        enable_correction_boluses: boolean, optional, default : False
            A flag that specifies whether to enable correction boluses during the replay of a given scenario.
        correction_boluses_handler: function, optional, default : corrects_above_250_handler
            A callback function that implements a corrective bolusing strategy during the replay of a given scenario.
        correction_boluses_handler_params: dict, optional, default : {}
            A dictionary that contains the parameters to pass to the correctionBolusesHandler function. It also serves as memory
            area for the correctionBolusesHandler function.

        save_suffix : str, optional, default : ''
            A string to be attached as suffix to the resulting output files' name.
        save_workspace : bool, optional, default : False
            A flag that specifies whether to save the workspace in the `results/workspace` folder.
        parallelize : boolean, optional, default : False
            A boolean that specifies whether to parallelize the identification process.
        n_processes : int, optional, default : None
            The number of processes to be spawn if `parallelize` is `True`.

        plot_mode : boolean, optional, default : True
            A boolean that specifies whether to show the plot of the results or not.
        verbose : boolean, optional, default : True
            A boolean that specifies the verbosity of ReplayBG.

        Returns
        -------
        None

        Raises
        ------
        None

        See Also
        --------
        None

        Examples
        --------
        None

        References
        --------
        Cappon et al., "ReplayBG: a methodology to identify a personalized model from type 1 diabetes data and simulate glucose concentrations to
        assess alternative therapies", IEEE TBME, 2023.
        """

        # Input validation
        input_validator = InputValidator(modality=modality, data=data, bw=bw, u2ss=u2ss, scenario=scenario, save_name=save_name,
                                         save_suffix=save_suffix,
                                         yts=yts, glucose_model=glucose_model, pathology=pathology, exercise=exercise,
                                         seed=seed,
                                         bolus_source=bolus_source, basal_source=basal_source, cho_source=cho_source,
                                         cgm_model=cgm_model,
                                         X0=X0,
                                         previous_data_name=previous_data_name,
                                         identification_method=identification_method,
                                         n_steps=n_steps, save_chains=save_chains, analyze_results=analyze_results,
                                         CR=CR, CF=CF, GT=GT,
                                         meal_generator_handler=meal_generator_handler,
                                         meal_generator_handler_params=meal_generator_handler_params,
                                         bolus_calculator_handler=bolus_calculator_handler,
                                         bolus_calculator_handler_params=bolus_calculator_handler_params,
                                         basal_handler=basal_handler, basal_handler_params=basal_handler_params,
                                         enable_hypotreatments=enable_hypotreatments,
                                         hypotreatments_handler=hypotreatments_handler,
                                         hypotreatments_handler_params=hypotreatments_handler_params,
                                         enable_correction_boluses=enable_correction_boluses,
                                         correction_boluses_handler=correction_boluses_handler,
                                         correction_boluses_handler_params=correction_boluses_handler_params,
                                         parallelize=parallelize, plot_mode=plot_mode, verbose=verbose)
        input_validator.validate()

        # Initialize core variables
        self.environment, self.model, self.identifier, self.dss = self.__init_core_variables(data=data, bw=bw, u2ss=u2ss,
                                                                                                     modality=modality,
                                                                                                     save_name=save_name,
                                                                                                     save_folder=save_folder,
                                                                                                     save_suffix=save_suffix,
                                                                                                     save_workspace=save_workspace,
                                                                                                     scenario=scenario,
                                                                                                     yts=yts,
                                                                                                     glucose_model=glucose_model,
                                                                                                     pathology=pathology,
                                                                                                     exercise=exercise,
                                                                                                     seed=seed,
                                                                                                     bolus_source=bolus_source,
                                                                                                     basal_source=basal_source,
                                                                                                     cho_source=cho_source,
                                                                                                     cgm_model=cgm_model,
                                                                                                     X0=X0,
                                                                                                     previous_data_name=previous_data_name,
                                                                                                     identification_method=identification_method,
                                                                                                     n_steps=n_steps,
                                                                                                     save_chains=save_chains,
                                                                                                     analyze_results=analyze_results,
                                                                                                     CR=CR, CF=CF,
                                                                                                     GT=GT,
                                                                                                     meal_generator_handler=meal_generator_handler,
                                                                                                     meal_generator_handler_params=meal_generator_handler_params,
                                                                                                     bolus_calculator_handler=bolus_calculator_handler,
                                                                                                     bolus_calculator_handler_params=bolus_calculator_handler_params,
                                                                                                     basal_handler=basal_handler,
                                                                                                     basal_handler_params=basal_handler_params,
                                                                                                     enable_hypotreatments=enable_hypotreatments,
                                                                                                     hypotreatments_handler=hypotreatments_handler,
                                                                                                     hypotreatments_handler_params=hypotreatments_handler_params,
                                                                                                     enable_correction_boluses=enable_correction_boluses,
                                                                                                     correction_boluses_handler=correction_boluses_handler,
                                                                                                     correction_boluses_handler_params=correction_boluses_handler_params,
                                                                                                     parallelize=parallelize,
                                                                                                     n_processes=n_processes,
                                                                                                     plot_mode=plot_mode,
                                                                                                     verbose=verbose)

        # ====================================================================

    def __init_core_variables(self, data, bw, u2ss, modality, save_name, save_folder, save_suffix, scenario,
                              yts, glucose_model, pathology, exercise, seed,
                              bolus_source, basal_source, cho_source,
                              cgm_model,
                              X0,
                              previous_data_name,
                              identification_method,
                              n_steps, save_chains, save_workspace, analyze_results,
                              CR, CF, GT,
                              meal_generator_handler, meal_generator_handler_params,
                              bolus_calculator_handler, bolus_calculator_handler_params,
                              basal_handler, basal_handler_params,
                              enable_hypotreatments, hypotreatments_handler, hypotreatments_handler_params,
                              enable_correction_boluses, correction_boluses_handler, correction_boluses_handler_params,
                              parallelize, n_processes, plot_mode, verbose):
        """
        Initializes the core variables (i.e., environment, model, mcmc, and dss) of ReplayBG.

        Parameters
        ----------
        data : pd.DataFrame
                Pandas dataframe which contains the data to be used by the tool.
        bw : double
            The patient's body weight.
        u2ss : double
            The steady state of the basal insulin infusion.
        modality : string
            A string that specifies if the function will be used to identify 
            the ReplayBG model on the given data or to replay the scenario specified by the given data
        save_name : string
            A string used to label, thus identify, each output file and result.
        save_suffix : string
            A string to be attached as suffix to the resulting output files' name.
        scenario: string
            A string that specifies whether the given scenario refers to a single-meal scenario or a multi-meal scenario
        yts: int
            An integer that specifies the data sample time (in minutes).
        glucose_model: string, {'IG','BG'}
            The model equation to be used as measured glucose.
        pathology: string, {'t1d', 't2d', 'pbh', 'healthy'}
            A string that specifies the patient pathology.
        exercise: boolean
            A boolean that specifies whether to simulate exercise or not.
        seed: int
            An integer that specifies the random seed. For reproducibility.
        bolus_source : string, {'data', or 'dss'}
            A string defining whether to use, during replay, the insulin bolus data contained in the 'data' timetable (if 'data'),
            or the boluses generated by the bolus calculator implemented via the provided 'bolusCalculatorHandler' function.
        basal_source : string, {'data', 'u2ss', or 'dss'}
            A string defining whether to use, during replay, the insulin basal data contained in the 'data' timetable (if 'data'), 
            or the basal generated by the controller implemented via the provided 'basalControllerHandler' function (if 'dss'), 
            or fixed to the average basal rate used during identification (if 'u2ss').
        cho_source : string, {'data', 'generated'}
            A string defining whether to use, during replay, the CHO data contained in the 'data' timetable (if 'data'),
            or the CHO generated by the meal generator implemented via the provided 'mealGeneratorHandler' function.
        cgm_model: string, {'CGM','IG'}
            A string that specify the cgm model selection.
            If IG is selected, CGM measure will be the noise-free IG state at the current time.

        X0: list
            The initial model state.

        n_steps: int
            Number of steps to use for the main chain. This is ignored if modality is 'replay'.
        save_chains: bool
            A flag that specifies whether to save the resulting mcmc chains and copula samplers.
        save_workspace: bool
            A flag that specifies whether to save the resulting workspace.
        analyze_results : bool
            A flag that specifies whether to analyze the resulting trace or not. Setting this flag to False will fasten
            ReplayBG and it is recommended if ReplayBG will be a component of a bigger framework (e.g., to be used in an
            iterative process).

        bolus_source : string, {'data', or 'dss'}
            A string defining whether to use, during replay, the insulin bolus data contained in the 'data' timetable (if 'data'),
            or the boluses generated by the bolus calculator implemented via the provided 'bolusCalculatorHandler' function.
        basal_source : string, {'data', 'u2ss', or 'dss'}
            A string defining whether to use, during replay, the insulin basal data contained in the 'data' timetable (if 'data'), 
            or the basal generated by the controller implemented via the provided 'basalControllerHandler' function (if 'dss'), 
            or fixed to the average basal rate used during identification (if 'u2ss').
        cho_source : string, {'data', 'generated'}
            A string defining whether to use, during replay, the CHO data contained in the 'data' timetable (if 'data'),
            or the CHO generated by the meal generator implemented via the provided 'mealGeneratorHandler' function.
        
        cgm_model: string, {'CGM','IG'}
            A string that specify the cgm model selection.
            If IG is selected, CGM measure will be the noise-free IG state at the current time.

        CR: double
            The carbohydrate-to-insulin ratio of the patient in g/U to be used by the integrated decision support system.
        CF: double
            The correction factor of the patient in mg/dl/U to be used by the integrated decision support system.
        GT: double
            The target glucose value in mg/dl to be used by the decsion support system modules.
        meal_generator_handler: function
            A callback function that implements a meal generator to be used during the replay of a given scenario.
        meal_generator_handler_params: dict
            A dictionary that contains the parameters to pass to the meal_generator_handler function.
        bolus_calculator_handler: function
            A callback function that implements a bolus calculator to be used during the replay of a given scenario.
        bolus_calculator_handler_params: dict
            A dictionary that contains the parameters to pass to the bolusCalculatorHandler function. It also serves as memory
            area for the bolusCalculatorHandler function.
        basal_handler: function
            A callback function that implements a basal controller to be used during the replay of a given scenario.
        basal_handler_params: dict
            A dictionary that contains the parameters to pass to the basalHandler function. It also serves as memory area for the basalHandler function.
        enable_hypotreatments: boolean
            A flag that specifies whether to enable hypotreatments during the replay of a given scenario.
        hypotreatments_handler: function
            A callback function that implements an hypotreatment strategy during the replay of a given scenario.
        hypotreatments_handler_params: dict
            A dictionary that contains the parameters to pass to the hypoTreatmentsHandler function. It also serves as memory
            area for the hypoTreatmentsHandler function.
        enable_correction_boluses: boolean
            A flag that specifies whether to enable correction boluses during the replay of a given scenario.
        correction_boluses_handler: function
            A callback function that implements a corrective bolusing strategy during the replay of a given scenario.
        correction_boluses_handler_params: dict
            A dictionary that contains the parameters to pass to the correctionBolusesHandler function. It also serves as memory
            area for the correctionBolusesHandler function.

        parallelize : boolean
            A boolean that specifies whether to parallelize the identification process.
        plot_mode : boolean
            A boolean that specifies whether to show the plot of the results or not.
        verbose : boolean
            A boolean that specifies the verbosity of ReplayBG.

        Returns
        -------
        environment: Environment
            An object that represents the hyperparameters to be used by ReplayBG environment.
        model: Model
            An object that represents the physiological model hyperparameters to be used by ReplayBG.
        mcmc: MCMC
            An object that represents the hyperparameters of the MCMC identification procedure.
        dss: DSS
            An object that represents the hyperparameters of the integrated decision support system.

        Raises
        ------
        None

        See Also
        --------
        None

        Examples
        --------
        None
        """

        # Initialize the environment parameters
        environment = Environment(modality=modality, save_name=save_name, save_folder=save_folder, save_suffix=save_suffix,
                                  save_workspace=save_workspace, analyze_results=analyze_results, scenario=scenario,
                                  bolus_source=bolus_source, basal_source=basal_source, cho_source=cho_source,
                                  cgm_model=cgm_model,
                                  seed=seed,
                                  parallelize=parallelize, n_processes=n_processes, plot_mode=plot_mode, verbose=verbose)

        # Initialize model
        if pathology == 't1d':
            if environment.scenario == 'single-meal':
                model = T1DModelSingleMeal(data=data, bw=bw, yts=yts, glucose_model=glucose_model, u2ss=u2ss, X0=X0, previous_data_name=previous_data_name, environment=environment, exercise=exercise, identification_method=identification_method)
            else:
                model = T1DModelMultiMeal(data=data, bw=bw, yts=yts, glucose_model=glucose_model, u2ss=u2ss, X0=X0, previous_data_name=previous_data_name, environment=environment, exercise=exercise, identification_method=identification_method)

        # Initialize identifier
        if identification_method == 'mcmc':
            identifier = MCMC(model,
                    n_steps=n_steps,
                    save_chains=save_chains,
                    callback_ncheck=1000)
        else:
            identifier = MAP(model,
                              max_iter=1500)


        # Initialize DSS
        dss = DSS(bw=bw, CR=CR, CF=CF, GT=GT,
                  meal_generator_handler=meal_generator_handler,
                  meal_generator_handler_params=meal_generator_handler_params,
                  bolus_calculator_handler=bolus_calculator_handler,
                  bolus_calculator_handler_params=bolus_calculator_handler_params,
                  basal_handler=basal_handler, basal_handler_params=basal_handler_params,
                  enable_hypotreatments=enable_hypotreatments, hypotreatments_handler=hypotreatments_handler,
                  hypotreatments_handler_params=hypotreatments_handler_params,
                  enable_correction_boluses=enable_correction_boluses,
                  correction_boluses_handler=correction_boluses_handler,
                  correction_boluses_handler_params=correction_boluses_handler_params)

        return environment, model, identifier, dss

    def run(self, data, bw, n_replay=1000, sensors=None):
        """
        Runs ReplayBG according to the chosen modality.

        Parameters
        ----------
        data: pd.DataFrame
            Pandas dataframe which contains the data to be used by the tool.
        bw: double
            The patient's body weight.
        n_replay: int, optional, default : 1000, {1000, 100, 10}
            The number of replay to be performed.
        sensors: list of Sensors
            The sensor to be used. If None, a new set of sensors is connected. This functionality can be used to keep
            using the same sensors over multiple ReplayBG runs (e.g. when working with intervals)
        Returns
        -------
        results: dict
            A dictionary containing the results of ReplayBG according to the chosen modality.

        Raises
        ------
        None

        See Also
        --------
        None

        Examples
        --------
        None
        """

        if self.environment.verbose:
            print('Running ReplayBG in `' + self.environment.modality + '` mode')

        # Unpack data to optimize performance
        rbg_data = ReplayBGData(data=data, rbg=self)

        # If modality is identification...
        if self.environment.modality == 'identification':
            # ...run identification
            if self.environment.verbose:
                print('Running model identification...')
            self.identifier.identify(data=data, rbg_data=rbg_data, rbg=self)

        # Load model parameters
        if self.environment.verbose:
            print('Loading identified model parameter realizations...')

        if type(self.identifier) is MCMC:
            with open(os.path.join(self.environment.replay_bg_path, 'results', 'draws',
                                   'draws_' + self.environment.save_name + '.pkl'), 'rb') as file:
                identification_results = pickle.load(file)
        else:
            with open(os.path.join(self.environment.replay_bg_path, 'results', 'map',
                                   'map_' + self.environment.save_name + '.pkl'), 'rb') as file:
                identification_results = pickle.load(file)
        draws = identification_results['draws']

        # Run replay
        if self.environment.verbose:
            print('Replaying scenario...')
        replayer = Replayer(rbg_data=rbg_data, draws=draws, n_replay=n_replay, rbg=self, sensors=sensors)
        glucose, x_end, cgm, insulin_bolus, correction_bolus, insulin_basal, cho, hypotreatments, meal_announcement, vo2, sensors = replayer.replay_scenario()

        analysis = dict()
        if self.environment.analyze_results:
            if self.environment.verbose:
                print('Analyzing results...')
            analysis = self.__analyze_results(glucose, cgm, insulin_bolus, correction_bolus, insulin_basal, cho, hypotreatments, meal_announcement, vo2, data)

        # Plot results if plot_mode is enabled
        if self.environment.plot_mode:

            if self.environment.verbose:
                print('Plotting results...')

            viz = Visualizer()
            viz.plot_replaybg_results(cgm=cgm, glucose=glucose, insulin_bolus=insulin_bolus,
                                      insulin_basal=insulin_basal,
                                      cho=cho, hypotreatments=hypotreatments, correction_bolus=correction_bolus,
                                      vo2=vo2, data=data, rbg=self)

        # Save results
        results = dict()
        results = self.__save_results(data, bw, glucose, x_end, cgm, insulin_bolus, correction_bolus, insulin_basal, cho, hypotreatments,
                            meal_announcement, vo2, sensors, analysis, self.environment.save_workspace)

        if self.environment.verbose:
            print('Done. Bye!')

        return results

    def __analyze_results(self, glucose, cgm, insulin_bolus, correction_bolus, insulin_basal, cho, hypotreatments, meal_announcement, vo2, data):
        """
        Analyzes ReplayBG results.

        Parameters
        ----------

        Returns
        -------

        Raises
        ------
        None

        See Also
        --------
        None

        Examples
        --------
        None
        """
        agata = Agata(glycemic_target='diabetes')

        analysis = dict()
        fields = ['median', 'ci5th', 'ci25th', 'ci75th', 'ci95th']
        for f in fields:
            analysis[f] = dict()


            # Transform the glucose profile under examination to a dataframe compatible with Agata
            glucose_profile = glucose_vector_to_dataframe(glucose[f], self.model.ts)

            # Analyse the glucose profile
            analysis[f]["glucose"] = agata.analyze_glucose_profile(glucose_profile)

            # Transform the cgm profile under examination to a dataframe compatible with Agata
            cgm_profile = glucose_vector_to_dataframe(cgm[f], self.model.yts)

            # Analyse the cgm profile
            analysis[f]["cgm"] = agata.analyze_glucose_profile(cgm_profile)


        total_insulin = np.zeros(shape=(insulin_bolus["realizations"].shape[0],))
        total_bolus_insulin = np.zeros(shape=(insulin_bolus["realizations"].shape[0],))
        total_correction_bolus_insulin = np.zeros(shape=(insulin_bolus["realizations"].shape[0],))
        total_basal_insulin = np.zeros(shape=(insulin_bolus["realizations"].shape[0],))

        total_cho = np.zeros(shape=(cho["realizations"].shape[0],))
        total_hypotreatments = np.zeros(shape=(cho["realizations"].shape[0],))
        total_meal_announcements = np.zeros(shape=(cho["realizations"].shape[0],))

        correction_bolus_insulin_number = np.zeros(shape=(insulin_bolus["realizations"].shape[0],))
        hypotreatment_number = np.zeros(shape=(cho["realizations"].shape[0],))

        exercise_session_number = np.zeros(shape=(vo2["realizations"].shape[0],))
        # TODO: add other metrics for exercise (e.g., average VO2 per session, duration of each session)

        for r in range(total_insulin.size):

            # Compute insulin amounts for each realization
            total_insulin[r] = np.sum(insulin_bolus["realizations"][r, :]) + np.sum(insulin_basal["realizations"][r, :])
            total_bolus_insulin[r] = np.sum(insulin_bolus["realizations"][r, :])
            total_basal_insulin[r] = np.sum(insulin_basal["realizations"][r, :])
            total_correction_bolus_insulin[r] = np.sum(correction_bolus["realizations"][r, :])

            # Compute CHO amounts for each realization
            total_cho[r] = np.sum(cho["realizations"][r, :])
            total_hypotreatments[r] = np.sum(hypotreatments["realizations"][r, :])
            total_meal_announcements[r] = np.sum(meal_announcement["realizations"][r, :])

            # Compute numbers for each realization
            correction_bolus_insulin_number[r] = np.where(correction_bolus["realizations"])[0].size
            hypotreatment_number[r] = np.where(hypotreatments["realizations"])[0].size

            # Compute exercise metrics for each realization
            e = np.where(hypotreatments["realizations"])[0]
            if e.size == 0:
                exercise_session_number[r] = 0
            else:
                d = np.diff(e)
                idxs = np.where(d > 1)[0]
                exercise_session_number[r] = 1 + idxs.size

        p = [50, 5, 25, 75, 95]
        for f in range(len(fields)):
            analysis[fields[f]]["event"] = dict()

            analysis[fields[f]]["event"]["total_insulin"] = np.percentile(total_insulin, p[f])
            analysis[fields[f]]["event"]["total_bolus_insulin"] = np.percentile(total_bolus_insulin, p[f])
            analysis[fields[f]]["event"]["total_basal_insulin"] = np.percentile(total_basal_insulin, p[f])
            analysis[fields[f]]["event"]["total_correction_bolus_insulin"] = np.percentile(total_correction_bolus_insulin, p[f])

            analysis[fields[f]]["event"]["total_cho"] = np.percentile(total_cho, p[f])
            analysis[fields[f]]["event"]["total_hypotreatments"] = np.percentile(total_hypotreatments, p[f])
            analysis[fields[f]]["event"]["total_meal_announcements"] = np.percentile(total_meal_announcements, p[f])

            analysis[fields[f]]["event"]["correction_bolus_insulin_number"] = np.percentile(correction_bolus_insulin_number, p[f])
            analysis[fields[f]]["event"]["hypotreatment_number"] = np.percentile(hypotreatment_number, p[f])

            analysis[fields[f]]["event"]["exercise_session_number"] = np.percentile(exercise_session_number, p[f])

        if self.environment.modality == 'identification':
            for f in fields:
                analysis[f]["identification"] = dict()

                data_hat = glucose_vector_to_dataframe(cgm[f], self.model.yts, pd.to_datetime(data.t.values[0]).to_pydatetime())

                analysis[f]["identification"]["rmse"] = rmse(data, data_hat)
                analysis[f]["identification"]["mard"] = mard(data, data_hat)
                analysis[f]["identification"]["clarke"] = clarke(data, data_hat)
                analysis[f]["identification"]["cod"] = cod(data, data_hat)
                analysis[f]["identification"]["g_rmse"] = g_rmse(data, data_hat)

        return analysis

    def __save_results(self, data, bw, glucose, x_end, cgm, insulin_bolus, correction_bolus, insulin_basal, cho,
                       hypotreatments, meal_announcement, vo2, sensors, analysis, save_workspace):
        """
        Save ReplayBG results.

        Parameters
        ----------

        Returns
        -------

        Raises
        ------
        None

        See Also
        --------
        None

        Examples
        --------
        None
        """
        results = dict()

        results['data'] = data
        results['bw'] = bw

        results['environment'] = self.environment
        results['identifier'] = self.identifier
        results['model'] = self.model
        results['dss'] = self.dss

        results['glucose'] = glucose
        results['x_end'] = x_end
        results['cgm'] = cgm
        results['insulin_bolus'] = insulin_bolus
        results['correction_bolus'] = correction_bolus
        results['insulin_basal'] = insulin_basal

        results['cho'] = cho
        results['hypotreatments'] = hypotreatments
        results['meal_announcement'] = meal_announcement
        results['vo2'] = vo2

        results['sensors'] = sensors

        results['analysis'] = analysis

        if self.environment.save_workspace:
            if self.environment.verbose:
                print('Saving results in ' + os.path.join(self.environment.replay_bg_path, 'results', 'workspaces',
                                                          self.environment.modality + '_' + self.environment.save_name + self.environment.save_suffix + '.pkl'))

            with open(os.path.join(self.environment.replay_bg_path, 'results', 'workspaces',
                                   self.environment.modality + '_' + self.environment.save_name + self.environment.save_suffix + '.pkl'),
                      'wb') as file:
                pickle.dump(results, file)

        return results