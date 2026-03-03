import unittest
from unittest.mock import patch
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from prompt_engine import model_v1, model_v2, model_v3

FAKE_RESPONSE = json.dumps({
    "input": {
        "pergunta": "fotossintese",
        "topico": "biologia",
        "nivel de complexidade": "basico",
        "requested_content": []
    },
    "output": {
        "titulo": "teste",
        "pontos_chave": []
    }
})

PROFILE = {
    "name": "teste",
    "idade": 25,
    "nivel de conhecimento": "intermediario",
    "estilo de aprendizagem": "leitura-escrita"
}

QUESTION = "Como funciona a fotossintese?"


class TestPromptBuilding(unittest.TestCase):

    @patch('prompt_engine.generate_response', return_value=FAKE_RESPONSE)
    def test_v1_sem_persona(self, mock_gen):
        prompt, _ = model_v1(PROFILE, QUESTION, "")
        self.assertNotIn("professor", prompt.lower())

    @patch('prompt_engine.generate_response', return_value=FAKE_RESPONSE)
    def test_v1_contem_pergunta(self, mock_gen):
        prompt, _ = model_v1(PROFILE, QUESTION, "")
        self.assertIn(QUESTION, prompt)

    @patch('prompt_engine.generate_response', return_value=FAKE_RESPONSE)
    def test_v2_persona_e_contexto(self, mock_gen):
        prompt, _ = model_v2(PROFILE, QUESTION, "")
        self.assertIn("professor experiente", prompt.lower())
        self.assertIn(str(PROFILE['idade']), prompt)
        self.assertIn(PROFILE['nivel de conhecimento'], prompt)

    @patch('prompt_engine.generate_response', return_value=FAKE_RESPONSE)
    def test_v3_chain_of_thought(self, mock_gen):
        prompt, _ = model_v3(PROFILE, QUESTION, "")
        for passo in ["Intuição inicial", "Conceito formal", "Exemplo guiado", "Conexão com conhecimento prévio"]:
            self.assertIn(passo, prompt)

    @patch('prompt_engine.generate_response', return_value=FAKE_RESPONSE)
    def test_v3_tem_persona(self, mock_gen):
        prompt, _ = model_v3(PROFILE, QUESTION, "")
        self.assertIn("professor experiente", prompt.lower())

    @patch('prompt_engine.generate_response', return_value=FAKE_RESPONSE)
    def test_prompts_sao_distintos(self, mock_gen):
        p1, _ = model_v1(PROFILE, QUESTION, "")
        p2, _ = model_v2(PROFILE, QUESTION, "")
        p3, _ = model_v3(PROFILE, QUESTION, "")
        self.assertNotEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        self.assertNotEqual(p2, p3)


if __name__ == '__main__':
    unittest.main()
