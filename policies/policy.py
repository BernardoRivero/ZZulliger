from policies.data_processor import DataProccesor
from policies.excel_handler import ExcelHandler
from typing import Any, List, Dict, Text, Optional
from rasa.core.featurizers.tracker_featurizers import TrackerFeaturizer
from rasa.core.policies.policy import PolicyPrediction, confidence_scores_for, \
    Policy
from rasa.shared.core.domain import Domain
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.utils.endpoints import *
from typing import Any, Text, Dict, List
from rasa.shared.core.events import SlotSet
from pathlib import Path

class ZulligerPolicy(Policy):

    def __init__(
            self,
            featurizer: Optional[TrackerFeaturizer] = None,
            priority: int = 2,
            should_finetune: bool = False,
            **kwargs: Any
    ) -> None:
        super().__init__(featurizer, priority, should_finetune, **kwargs)
        
        ## Maneja todo lo relacionado a excel
        self._excelHandler = ExcelHandler()

        ## Procesa contenidos y determinantes
        self._data_processor = DataProccesor()
        
        ## Indicador de etapa 
        self._state = 1        
        # Indicador de respuesta
        self._lamina = 1
        # Respuestas del entrevistado
        self._responses_lamina1 = []
        self._responses_lamina2 = []
        self._responses_lamina3 = []
        # Razones del entrevistado
        self._reasons_lamina1 = []
        self._reasons_lamina2 = []
        self._reasons_lamina3 = []

        self._counter = 0
        
    def train(
            self,
            training_trackers: List[TrackerWithCachedStates],
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any
    ) -> None:
        pass

    def get_project_root(self) -> Path:
        return Path(__file__).parent.parent

    def predict_action_probabilities(
            self, 
            tracker: DialogueStateTracker,
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any
            
    ) -> "PolicyPrediction":
        intent = tracker.latest_message.intent
        
        # If the last thing rasa did was listen to a user message, we need to
        # send back a response.    
        if tracker.latest_action_name == "action_listen":
            print(intent["name"])

            ##self._excelHandler.update_data()

            # The user starts the conversation.
            if intent["name"] == "welcome":
                return self._prediction(confidence_scores_for('utter_nombre', 1.0, domain))

            # The user enters his name.
            elif intent["name"] == "id":
                slot_nombre = str(tracker.get_slot("nombre"))
                self._excelHandler.create_excel_sheet(slot_nombre)
                return self._prediction(confidence_scores_for('utter_welcome', 1.0, domain))

            # The test starts, the first image is displayed.
            elif intent["name"] == "start":
                return self._prediction(confidence_scores_for('utter_start', 1.0, domain))

            if intent["name"] == "termine":
                if self._lamina == 1:
                    self._lamina = 2
                    return self._prediction(confidence_scores_for("utter_Lamina2", 1.0, domain))
                elif self._lamina == 2:
                    self._lamina = 3
                    return self._prediction(confidence_scores_for("utter_Lamina3", 1.0, domain))
                elif self._lamina == 3:
                    self._lamina = 1
                    self._state = 2
                    self._counter = 0
                    tracker.update(SlotSet("respuestaLamina1", self._responses_lamina1[self._counter]))

                    print(str(self._responses_lamina1))
                    print(str(self._responses_lamina2))
                    print(str(self._responses_lamina3)) 

                    return self._prediction(confidence_scores_for("utter_Lamina1Razones", 1.0, domain))

            # The user enters what he sees in the images.
            if intent["name"] == "respuestasv" or intent["name"] == "respuestasvmas" or intent["name"] == "respuestaso" or intent["name"] == "respuestas+":
                
                #self._data_processor.process(self._lamina, tracker)
                if self._state == 1:     ## Etapa de respuesta
                    
                    #self._data_processor.process_developmental_quality(intent["name"], self._lamina-1)
                    
                    if self._lamina == 1:                        
                        #tracker.update(SlotSet("respuestaLamina1", tracker.latest_message.text))
                        self._responses_lamina1.append(tracker.latest_message.text)
                        if len(self._responses_lamina1) == 5:
                            self._lamina = 2
                            return self._prediction(confidence_scores_for("utter_Lamina2", 1.0, domain))
                        
                        #return self._prediction(confidence_scores_for("utter_Lamina2", 1.0, domain))
                    
                    elif self._lamina == 2:
                        # tracker.update(SlotSet("respuestaLamina2", tracker.latest_message.text))
                        # return self._prediction(confidence_scores_for("utter_Lamina3", 1.0, domain))
                        self._responses_lamina2.append(tracker.latest_message.text)
                        if len(self._responses_lamina2) == 5:
                            self._lamina = 3
                            return self._prediction(confidence_scores_for("utter_Lamina3", 1.0, domain))

                    elif self._lamina == 3:                        
                        self._responses_lamina3.append(tracker.latest_message.text)
                        if len(self._responses_lamina3) == 5:
                            self._lamina = 1
                            self._state = 2
                            self._counter = 0
                            tracker.update(SlotSet("respuestaLamina1", self._responses_lamina1[self._counter]))

                            print(str(self._responses_lamina1))
                            print(str(self._responses_lamina2))
                            print(str(self._responses_lamina3))

                            return self._prediction(confidence_scores_for("utter_Lamina1Razones", 1.0, domain))

                        # tracker.update(SlotSet("respuestaLamina3", tracker.latest_message.text))
                        # return self._prediction(confidence_scores_for("utter_Lamina1Razones", 1.0, domain))
               
                elif self._state == 2:  ## Etapa de revisión    
                    self._counter += 1
                    
                    if self._lamina == 1:
                        self._reasons_lamina1.append(tracker.latest_message.text)
                        if self._counter < len(self._responses_lamina1):
                            tracker.update(SlotSet("respuestaLamina1", self._responses_lamina1[self._counter]))
                            return self._prediction(confidence_scores_for("utter_Lamina1Razones2", 1.0, domain))
                        else:
                            self._lamina += 1
                            self._counter = 0
                            tracker.update(SlotSet("respuestaLamina2", self._responses_lamina2[self._counter]))
                            return self._prediction(confidence_scores_for("utter_Lamina2Razones", 1.0, domain))
                    
                    elif self._lamina == 2:                        
                        self._reasons_lamina2.append(tracker.latest_message.text)
                        if self._counter < len(self._responses_lamina2):
                            tracker.update(SlotSet("respuestaLamina2", self._responses_lamina2[self._counter]))
                            return self._prediction(confidence_scores_for("utter_Lamina2Razones", 1.0, domain))
                        else:
                            self._lamina += 1
                            self._counter = 0
                            tracker.update(SlotSet("respuestaLamina3", self._responses_lamina3[self._counter]))
                            return self._prediction(confidence_scores_for("utter_Lamina3Razones", 1.0, domain))

                    elif self._lamina == 3:
                        self._reasons_lamina3.append(tracker.latest_message.text)
                        if self._counter < len(self._responses_lamina3):
                            tracker.update(SlotSet("respuestaLamina3", self._responses_lamina3[self._counter]))
                            return self._prediction(confidence_scores_for("utter_Lamina3Razones", 1.0, domain))
                        else:
                            self._lamina = 1
                            self._counter = 0
                            self._state = 3
                            return self._prediction(confidence_scores_for("utter_TercerParte", 1.0, domain))
                                   
            if intent["name"] == "ok":
                if self._state == 3:    ## Etapa de dibujo
                    
                    if self._lamina == 1:
                        if self._counter < len(self._responses_lamina1):
                            tracker.update(SlotSet("respuestaLamina1", self._responses_lamina1[self._counter]))
                            self._counter += 1
                            return self._prediction(confidence_scores_for("utter_TercerParteLamina1", 1.0, domain))
                        else:
                            self._counter = 0
                            self._lamina += 1
                            tracker.update(SlotSet("respuestaLamina2", self._responses_lamina2[self._counter]))
                            return self._prediction(confidence_scores_for("utter_TercerParteLamina2", 1.0, domain))

                    elif self._lamina == 2:
                        self._counter += 1
                        if self._counter < len(self._responses_lamina2):                            
                            tracker.update(SlotSet("respuestaLamina2", self._responses_lamina2[self._counter]))                            
                            return self._prediction(confidence_scores_for("utter_TercerParteLamina2", 1.0, domain))
                        else:
                            self._counter = 0
                            self._lamina += 1
                            tracker.update(SlotSet("respuestaLamina3", self._responses_lamina3[self._counter]))
                            return self._prediction(confidence_scores_for("utter_TercerParteLamina3", 1.0, domain))
                    
                    elif self._lamina == 3:
                        self._counter += 1
                        if self._counter < len(self._responses_lamina3):
                            tracker.update(SlotSet("respuestaLamina3", self._responses_lamina3[self._counter]))
                            return self._prediction(confidence_scores_for("utter_TercerParteLamina3", 1.0, domain))
                        
                        else:       ## Final 
                            self._state = 1
                            self._lamina = 1
                            self._counter = 0
                            return self._prediction(confidence_scores_for("utter_Fin", 1.0, domain))
        
        # If rasa latest action isn't "action_listen", it means the last thing
        # rasa did was send a response, so now we need to listen again so the
        # user can talk to us.
        return self._prediction(confidence_scores_for(
            "action_listen", 1.0, domain
        ))

    def _metadata(self) -> Dict[Text, Any]:
        return {
            "priority": 2
        }

    @classmethod
    def _metadata_filename(cls) -> Text:
        return "zulliger_policy.json"