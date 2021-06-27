#from actions.actions import imprimirSlot
#import json
from typing import Any, List, Dict, Text, Optional
import pandas as pd
from pandas import ExcelWriter
from rasa.core.featurizers.tracker_featurizers import TrackerFeaturizer
from rasa.core.policies.policy import PolicyPrediction, confidence_scores_for, \
    Policy
from rasa.shared.core.domain import Domain
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.utils.endpoints import *
from typing import Any, Text, Dict, List
#from rasa_sdk.executor import CollectingDispatcher

from rasa.shared.core.events import SlotSet

class TestPolicy(Policy):

    def __init__(
            self,
            featurizer: Optional[TrackerFeaturizer] = None,
            priority: int = 2,
            should_finetune: bool = False,
            **kwargs: Any
    ) -> None:
        super().__init__(featurizer, priority, should_finetune, **kwargs)
        
        #indicador de respuesta
        self._contador = 0
        #respuestas del entrevistado
        self._respuesta1 = ""
        self._respuesta2 = ""
        self._respuesta3 = ""
        
        planilla = pd.DataFrame({'Lám': [''],
                   'N°Rta':[''],
                   'N°Loc':[''],
                   'Loc': [''],
                   'DQ': [''],
                   'Det': [''],
                   'FQ': [''],
                   '(2)': [''],
                   'Cont': [''],
                   'Pop': [''],
                   'Pje Z': [''],
                   'CCEE': ['']})
        planilla = planilla[['Lám', 'N°Rta', 'N°Loc','Loc','DQ','Det','FQ','(2)','Cont','Pop','Pje Z','CCEE']]
        writer = ExcelWriter('C:/Users/Bernardo/Desktop/Zulliger/PlanillaZulliger.xlsx')
        planilla.to_excel(writer, 'Hoja de datos', index=False)
        writer.save()
    def train(
            self,
            training_trackers: List[TrackerWithCachedStates],
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any
    ) -> None:
        pass

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
            # The user starts the conversation.
            if intent["name"] == "welcome":
                return self._prediction(confidence_scores_for('utter_welcome', 1.0, domain))

            # The user enters "listo".
            if intent["name"] == "start":
                return self._prediction(confidence_scores_for('utter_start', 1.0, domain))

            # The user enters a response.
            if intent["name"] == "respuestas":
                self._contador = self._contador + 1
                tracker.update(SlotSet("contador", self._contador))
                if self._contador == 1:
                    
                    # Guarda en la variable "respuesta1" SOLO el texto que ingreso el usuario
                    self._respuesta1 = tracker.latest_message.text

                    # Setea el slot "respuestaLamina1" con lo que ingreso el usuario
                    tracker.update(SlotSet("respuestaLamina1", self._respuesta1))
                    # Guarda en el slot "response" la próxima respuesta del bot 
                    # (se manda en la action "action_imprimir_determinantes")
                    tracker.update(SlotSet("response", "utter_Lamina2"))
                
                # Lo mismo se hace con las respuestas 2 y 3:
                elif self._contador == 2:
                    self._respuesta2 = tracker.latest_message.text
                    tracker.update(SlotSet("respuestaLamina2", self._respuesta2))
                    tracker.update(SlotSet("response", "utter_Lamina3"))

                elif self._contador == 3:
                    tracker.update(SlotSet("contador", 3))
                    self._respuesta3 = tracker.latest_message.text
                    tracker.update(SlotSet("respuestaLamina3", self._respuesta3))
                    
                    # Acá empieza la parte de revisión de las láminas 
                    tracker.update(SlotSet("response", "utter_Lamina1Razones"))
                if self._contador < 4:
                    return self._prediction(confidence_scores_for("action_imprimir_determinantes", 1.0, domain))
                elif self._contador < 7:
                    if self._contador == 4:
                        tracker.update(SlotSet("contador", 1))
                        self._razones1 = tracker.latest_message.text
                        tracker.update(SlotSet("razonesLamina1", self._respuesta3))
                        tracker.update(SlotSet("response", "utter_Lamina2Razones"))
                    elif self._contador == 5:
                         tracker.update(SlotSet("contador", 2))
                         self._razones2 = tracker.latest_message.text
                         tracker.update(SlotSet("razonesLamina2", self._respuesta3))
                         tracker.update(SlotSet("response", "utter_Lamina3Razones"))
                    else:
                         tracker.update(SlotSet("contador", 3))
                    return self._prediction(confidence_scores_for("action_imprimir_determinantes", 1.0, domain))
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
        return "test_policy.json"