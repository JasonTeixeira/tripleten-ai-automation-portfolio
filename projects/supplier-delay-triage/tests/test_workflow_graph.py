"""Check that the exported workflow exposes the reviewer-required routing."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WorkflowGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(
            (ROOT / 'workflows/supplier-delay-triage.json').read_text()
        )
        cls.nodes = {n['name']: n for n in cls.workflow['nodes']}

    def switch(self):
        matches = [n for n in self.workflow['nodes'] if n['type'] == 'n8n-nodes-base.switch']
        self.assertEqual(len(matches), 1, 'Expose the three outcomes through a native n8n Switch')
        return matches[0]

    def test_three_explicit_route_conditions(self):
        node = self.switch()
        rules = node['parameters']['rules']['values']
        expected = [('exception', 'Exception'), ('logged', 'Routine Log'), ('manual_review', 'Manual Review')]
        self.assertEqual(len(rules), 3)
        for rule, (value, label) in zip(rules, expected):
            condition = rule['conditions']['conditions'][0]
            self.assertEqual(condition['leftValue'], '={{ $json.route }}')
            self.assertEqual(condition['rightValue'], value)
            self.assertEqual(condition['operator'], {'type': 'string', 'operation': 'equals'})
            self.assertEqual(rule['outputKey'], label)

    def test_outcomes_connected_to_visible_branches(self):
        switch = self.switch()
        outputs = self.workflow['connections'][switch['name']]['main']
        self.assertEqual([items[0]['node'] for items in outputs[:3]], ['Exception', 'Routine Log', 'Manual Review'])
        for label in ['Exception', 'Routine Log', 'Manual Review']:
            self.assertEqual(self.nodes[label]['type'], 'n8n-nodes-base.noOp')

    def test_unmatched_routes_fall_back_to_manual_review(self):
        switch = self.switch()
        self.assertEqual(switch['parameters']['options']['fallbackOutput'], 'extra')
        fallback = self.workflow['connections'][switch['name']]['main'][3]
        self.assertEqual(fallback[0]['node'], 'Manual Review')

    def test_intake_and_persistence_surround_real_llm_call(self):
        self.assertEqual(self.nodes['Fetch Supplier Emails']['parameters']['url'], 'http://ledger:8091/intake')
        self.assertEqual(self.nodes['One Email Per Item']['parameters']['fieldToSplitOut'], 'messages')
        self.assertIn('JSON.stringify(item.json)', self.nodes['Prepare AI Request']['parameters']['jsCode'])
        self.assertEqual(self.nodes['Extract With Local LLM']['parameters']['url'], 'http://ollama:11434/api/chat')
        self.assertEqual(self.nodes['Validate Route And Record']['parameters']['url'], 'http://ledger:8091/record')
        next_node = self.workflow['connections']['Validate Route And Record']['main'][0][0]['node']
        self.assertEqual(next_node, self.switch()['name'])


if __name__ == '__main__':
    unittest.main()
