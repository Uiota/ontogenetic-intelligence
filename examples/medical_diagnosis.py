#!/usr/bin/env python3
"""
OGI Medical Diagnosis Example
Demonstrates OGI agents collaboratively developing diagnostic capabilities
while maintaining patient privacy and regulatory compliance.

Scenario: 5 hospitals developing shared diagnostic intelligence for rare diseases
without sharing patient data or requiring constant connectivity.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ogi_simulation import OGIAgent
import random
import json

class MedicalDiagnosticAgent(OGIAgent):
    """
    Specialized OGI agent for medical diagnosis development
    """

    def __init__(self, hospital_id, patient_population):
        super().__init__(f"hospital_{hospital_id}", "medical_diagnosis")
        self.hospital_id = hospital_id
        self.patient_population = patient_population
        self.diagnostic_frameworks = {
            'symptom_pattern_recognition': 0.6,
            'risk_factor_assessment': 0.55,
            'differential_diagnosis': 0.5,
            'rare_disease_detection': 0.4,
            'treatment_response_prediction': 0.45
        }
        self.case_history = []

    def process_patient_case(self, symptoms, demographics, outcome=None):
        """
        Process a patient case and learn from the experience
        Note: This uses synthetic data - no real patient information
        """
        case = {
            'case_id': f"case_{len(self.case_history)}",
            'symptoms': symptoms,
            'demographics': demographics,
            'hospital': self.hospital_id,
            'epoch': self.epoch
        }

        # Generate diagnostic hypothesis
        hypothesis = self.generate_diagnostic_hypothesis(case)

        # Test against known outcome (if available)
        if outcome:
            result = self.validate_diagnosis(hypothesis, outcome)
            self.integrate_diagnostic_learning(result)
            case['outcome'] = outcome
            case['hypothesis'] = hypothesis
            case['validation'] = result

        self.case_history.append(case)
        return hypothesis

    def generate_diagnostic_hypothesis(self, case):
        """
        Generate diagnostic hypothesis based on current frameworks
        """
        symptoms = case['symptoms']
        demographics = case['demographics']

        # Simulate pattern recognition based on current frameworks
        confidence = self.diagnostic_frameworks['symptom_pattern_recognition']

        # Example diagnostic reasoning
        if 'chest_pain' in symptoms and 'shortness_of_breath' in symptoms:
            if demographics.get('age', 0) > 60:
                hypothesis = {
                    'primary_diagnosis': 'cardiac_event',
                    'confidence': confidence * 0.9,
                    'supporting_symptoms': ['chest_pain', 'shortness_of_breath'],
                    'risk_factors': ['age'],
                    'framework_used': 'symptom_pattern_recognition'
                }
            else:
                hypothesis = {
                    'primary_diagnosis': 'anxiety_disorder',
                    'confidence': confidence * 0.7,
                    'supporting_symptoms': ['chest_pain', 'shortness_of_breath'],
                    'risk_factors': [],
                    'framework_used': 'symptom_pattern_recognition'
                }
        else:
            # More complex diagnostic reasoning
            hypothesis = {
                'primary_diagnosis': 'requires_further_investigation',
                'confidence': confidence * 0.5,
                'supporting_symptoms': symptoms,
                'risk_factors': list(demographics.keys()),
                'framework_used': 'differential_diagnosis'
            }

        return hypothesis

    def validate_diagnosis(self, hypothesis, actual_outcome):
        """
        Validate diagnostic hypothesis against actual outcome
        """
        correct = hypothesis['primary_diagnosis'] == actual_outcome['diagnosis']
        confidence_accuracy = abs(hypothesis['confidence'] - actual_outcome.get('certainty', 0.5))

        return {
            'correct': correct,
            'confidence_error': confidence_accuracy,
            'learning_value': 0.9 if correct else 0.3,
            'framework_effectiveness': hypothesis['confidence'] if correct else 0.2
        }

    def integrate_diagnostic_learning(self, validation_result):
        """
        Integrate learning from diagnostic validation
        """
        if validation_result['correct']:
            # Strengthen successful frameworks
            framework = validation_result.get('framework_used', 'general')
            if framework in self.diagnostic_frameworks:
                improvement = 0.05 * validation_result['learning_value']
                self.diagnostic_frameworks[framework] = min(0.95,
                    self.diagnostic_frameworks[framework] + improvement)
        else:
            # Modest adjustment for incorrect diagnoses
            for framework in self.diagnostic_frameworks:
                adjustment = -0.01 * (1 - validation_result['confidence_error'])
                self.diagnostic_frameworks[framework] = max(0.1,
                    self.diagnostic_frameworks[framework] + adjustment)

    def extract_diagnostic_insights(self):
        """
        Extract diagnostic insights for knowledge sharing
        Does not include patient data - only learned patterns
        """
        return {
            'hospital_id': self.hospital_id,
            'diagnostic_frameworks': self.diagnostic_frameworks.copy(),
            'cases_processed': len(self.case_history),
            'population_characteristics': self.patient_population,
            'successful_patterns': self.get_successful_patterns(),
            'confidence_metrics': self.calculate_diagnostic_confidence()
        }

    def get_successful_patterns(self):
        """
        Extract successful diagnostic patterns without patient data
        """
        patterns = {}
        for case in self.case_history:
            if case.get('validation', {}).get('correct', False):
                pattern_key = case['hypothesis']['primary_diagnosis']
                if pattern_key not in patterns:
                    patterns[pattern_key] = {
                        'success_count': 0,
                        'common_symptoms': [],
                        'risk_factors': []
                    }
                patterns[pattern_key]['success_count'] += 1
                patterns[pattern_key]['common_symptoms'].extend(
                    case['hypothesis']['supporting_symptoms'])
                patterns[pattern_key]['risk_factors'].extend(
                    case['hypothesis']['risk_factors'])

        return patterns

    def calculate_diagnostic_confidence(self):
        """
        Calculate overall diagnostic confidence metrics
        """
        if not self.case_history:
            return {'overall_accuracy': 0.5, 'total_cases': 0}

        correct_cases = sum(1 for case in self.case_history
                          if case.get('validation', {}).get('correct', False))

        return {
            'overall_accuracy': correct_cases / len(self.case_history),
            'total_cases': len(self.case_history),
            'framework_maturity': sum(self.diagnostic_frameworks.values()) / len(self.diagnostic_frameworks)
        }


def run_medical_diagnosis_simulation():
    """
    Run a complete medical diagnosis simulation
    """
    print("🏥 Medical Diagnosis OGI Simulation")
    print("=" * 50)

    # Initialize hospitals with different patient populations
    hospitals = [
        MedicalDiagnosticAgent(1, "rural_mining_community"),
        MedicalDiagnosticAgent(2, "urban_elderly"),
        MedicalDiagnosticAgent(3, "pediatric_specialized"),
        MedicalDiagnosticAgent(4, "cardiac_center"),
        MedicalDiagnosticAgent(5, "general_population")
    ]

    # Simulate patient cases over 15 epochs
    synthetic_cases = generate_synthetic_cases()

    for epoch in range(15):
        print(f"\n📅 Epoch {epoch + 1}: Processing patient cases...")

        for hospital in hospitals:
            # Each hospital processes 2-5 cases per epoch
            num_cases = random.randint(2, 5)

            for _ in range(num_cases):
                case = random.choice(synthetic_cases)
                hypothesis = hospital.process_patient_case(
                    case['symptoms'],
                    case['demographics'],
                    case['outcome']
                )

            # Agent development cycle
            hospital.develop_epoch()

        # Knowledge sharing every 5 epochs (deferred sync)
        if epoch % 5 == 0 and epoch > 0:
            print(f"🔄 Knowledge sharing session (Epoch {epoch + 1})")
            share_medical_knowledge(hospitals)

    # Final analysis
    print("\n📊 Final Diagnostic Capabilities:")
    for hospital in hospitals:
        metrics = hospital.calculate_diagnostic_confidence()
        print(f"   Hospital {hospital.hospital_id} ({hospital.patient_population}):")
        print(f"     Accuracy: {metrics['overall_accuracy']:.1%}")
        print(f"     Cases: {metrics['total_cases']}")
        print(f"     Framework Maturity: {metrics['framework_maturity']:.3f}")


def generate_synthetic_cases():
    """
    Generate synthetic patient cases for simulation
    Note: These are completely artificial and not based on real medical data
    """
    return [
        {
            'symptoms': ['chest_pain', 'shortness_of_breath'],
            'demographics': {'age': 65, 'gender': 'M'},
            'outcome': {'diagnosis': 'cardiac_event', 'certainty': 0.9}
        },
        {
            'symptoms': ['chest_pain', 'shortness_of_breath', 'anxiety'],
            'demographics': {'age': 25, 'gender': 'F'},
            'outcome': {'diagnosis': 'anxiety_disorder', 'certainty': 0.8}
        },
        {
            'symptoms': ['fever', 'cough', 'fatigue'],
            'demographics': {'age': 35, 'gender': 'M'},
            'outcome': {'diagnosis': 'viral_infection', 'certainty': 0.7}
        },
        {
            'symptoms': ['headache', 'vision_changes', 'nausea'],
            'demographics': {'age': 45, 'gender': 'F'},
            'outcome': {'diagnosis': 'migraine', 'certainty': 0.75}
        },
        {
            'symptoms': ['joint_pain', 'stiffness', 'swelling'],
            'demographics': {'age': 55, 'gender': 'F'},
            'outcome': {'diagnosis': 'rheumatoid_arthritis', 'certainty': 0.85}
        }
    ]


def share_medical_knowledge(hospitals):
    """
    Simulate supervised knowledge sharing between hospitals
    Only patterns and insights are shared, never patient data
    """
    print("   🔒 Privacy-preserving knowledge extraction...")

    # Extract insights from each hospital
    insights = []
    for hospital in hospitals:
        insight = hospital.extract_diagnostic_insights()
        insights.append(insight)

    print("   🧠 Knowledge integration...")

    # Each hospital learns from aggregated insights
    for hospital in hospitals:
        # Simulate learning from other hospitals' patterns
        for insight in insights:
            if insight['hospital_id'] != hospital.hospital_id:
                # Learn from successful patterns of other hospitals
                for framework, value in insight['diagnostic_frameworks'].items():
                    if framework in hospital.diagnostic_frameworks:
                        # Conservative learning from external knowledge
                        improvement = 0.02 * (value - hospital.diagnostic_frameworks[framework])
                        hospital.diagnostic_frameworks[framework] = min(0.95,
                            hospital.diagnostic_frameworks[framework] + improvement)

    print("   ✅ Knowledge sharing complete (no patient data exchanged)")


if __name__ == "__main__":
    run_medical_diagnosis_simulation()