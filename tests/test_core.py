"""
EditalShield - Unit Tests
Tests for core functionality
"""

import pytest
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestMemorialProtector:
    """Tests for Memorial Protector module"""
    
    @pytest.fixture
    def protector(self):
        from editalshield.modules.memorial_protector import MemorialProtector
        return MemorialProtector()
    
    @pytest.fixture
    def sample_text(self):
        return """
        Nossa solução utiliza algoritmo BehaviorAnalyzer V2 com parâmetros W=0.7.
        Dataset privado de 2M transações com acurácia 94.2%.
        Contato: dr.silva@techvision.com
        """
    
    def test_entropy_calculation(self, protector):
        """Test Shannon entropy calculation"""
        text = "hello world hello"
        entropy, entropy_norm = protector.calculate_entropy(text)
        
        assert entropy >= 0
        assert 0 <= entropy_norm <= 1
        
    def test_zipf_score(self, protector):
        """Test Zipfian deviation score"""
        # Common text (low score - mostly stop words)
        common = "Eu sou você e nós somos eles para sempre com isso."
        score_common = protector.calculate_zipf_score(common)
        
        # Technical text (high score)
        technical = "Eigenvectors ortogonais com decomposição SVD e hiperparâmetros."
        score_tech = protector.calculate_zipf_score(technical)
        
        assert score_tech > score_common
        assert 0 <= score_common <= 1
        assert 0 <= score_tech <= 1
    
    def test_pattern_detection_algorithm(self, protector):
        """Test algorithm pattern detection"""
        text = "Nosso algoritmo BehaviorAnalyzer V2 é proprietário"
        patterns = protector.detect_sensitive_patterns(text)
        
        assert 'algorithm' in patterns
        assert len(patterns['algorithm']) > 0
    
    def test_pattern_detection_parameters(self, protector):
        """Test parameter pattern detection"""
        text = "Parâmetros W=0.7, K=1.5, threshold=0.8"
        patterns = protector.detect_sensitive_patterns(text)
        
        assert 'parameters' in patterns
    
    def test_pattern_detection_email(self, protector):
        """Test email pattern detection"""
        text = "Contato: joao.silva@empresa.com"
        patterns = protector.detect_sensitive_patterns(text)
        
        assert 'contacts' in patterns
    
    def test_section_classification(self, protector):
        """Test section type classification"""
        technical = "Desenvolvemos algoritmo de machine learning"
        market = "O mercado está em expansão de 25% a.a."
        team = "Nossa equipe tem CTO formado no MIT"
        
        assert protector.classify_section(technical) == 'technical'
        assert protector.classify_section(market) == 'market'
        assert protector.classify_section(team) == 'team'
    
    def test_risk_score_range(self, protector):
        """Test that risk score is in valid range"""
        score = protector.calculate_risk_score(0.5, 3, 'technical')
        assert 0 <= score <= 100
    
    def test_paragraph_analysis(self, protector):
        """Test single paragraph analysis"""
        text = "Algoritmo BehaviorAnalyzer V2 com parâmetros W=0.7"
        analysis = protector.analyze_paragraph(text, 0)
        
        assert analysis.index == 0
        assert analysis.risk_score >= 0
        assert len(analysis.sensitive_patterns) > 0
    
    def test_memorial_analysis(self, protector, sample_text):
        """Test complete memorial analysis"""
        analysis = protector.analyze_memorial(sample_text)
        
        assert analysis.total_paragraphs > 0
        assert analysis.overall_risk_score >= 0
        assert len(analysis.paragraphs) > 0
    
    def test_text_protection(self, protector):
        """Test sensitive text replacement"""
        text = "Email: teste@email.com"
        patterns = {'contacts': ['teste@email.com']}
        protected = protector.protect_text(text, patterns)
        
        assert 'teste@email.com' not in protected
        assert '[CONTATO OMITIDO]' in protected
    
    def test_report_generation(self, protector, sample_text):
        """Test report generation"""
        analysis = protector.analyze_memorial(sample_text)
        
        text_report = protector.generate_report(analysis, 'text')
        json_report = protector.generate_report(analysis, 'json')
        
        assert 'EDITALSHIELD' in text_report
        assert 'risk_score' in json.loads(json_report) or 'overall_risk_score' in json.loads(json_report)


class TestSyntheticDataGenerator:
    """Tests for synthetic data generator"""
    
    @pytest.fixture
    def generator(self):
        sys.path.insert(0, '.')
        from database.generate_synthetic_data import SyntheticDataGenerator
        return SyntheticDataGenerator(seed=42)
    
    def test_entropy_calculation(self, generator):
        """Test entropy calculation"""
        text = "hello world hello world"
        entropy = generator.calculate_entropy(text)
        assert entropy >= 0
    
    def test_edital_generation(self, generator):
        """Test edital generation"""
        edital = generator.generate_edital()
        
        assert 'name' in edital
        assert 'agency' in edital
        assert 'min_value' in edital
        assert edital['min_value'] > 0
    
    def test_memorial_generation(self, generator):
        """Test memorial generation"""
        memorial = generator.generate_memorial()
        
        assert 'sector' in memorial
        assert 'paragraphs' in memorial
        assert len(memorial['paragraphs']) > 0
    
    def test_dataset_generation(self, generator):
        """Test full dataset generation"""
        dataset = generator.generate_dataset(num_memorials=5, num_editals=10)
        
        assert len(dataset['editals']) == 10
        assert len(dataset['memorials']) == 5


class TestBayesianTrainer:
    """Tests for Bayesian model trainer"""
    
    @pytest.fixture
    def sample_data_path(self, tmp_path):
        """Create sample training data"""
        data = {
            'editals': [{'name': 'Test', 'agency': 'TEST'}],
            'memorials': [
                {
                    'id': 1,
                    'sector': 'software',
                    'paragraphs': [
                        {
                            'index': 0,
                            'section': 'technical',
                            'text': 'Test paragraph',
                            'has_exposure': True,
                            'stats': {'entropy_normalized': 0.5}
                        }
                    ]
                }
            ]
        }
        
        filepath = tmp_path / 'test_data.json'
        with open(filepath, 'w') as f:
            json.dump(data, f)
        
        return str(filepath)
    
    def test_data_loading(self, sample_data_path):
        """Test training data loading"""
        sys.path.insert(0, '.')
        from models.train_bayesian_model import BayesianModelTrainer
        
        trainer = BayesianModelTrainer(output_dir='./models')
        df = trainer.load_training_data_from_json(sample_data_path)
        
        assert len(df) > 0


class TestEditalMatcher:
    """Tests for Edital Matcher"""
    
    @pytest.fixture
    def matcher(self):
        from editalshield.modules.edital_matcher import EditalMatcher
        
        # Mock data
        editals = [
            {
                'name': 'Edital Agritech Inovação',
                'agency': 'FINEP',
                'eligible_sectors': ['agritech', 'biotech', 'agricultura'],
                'eligible_stages': ['seed'],
                'min_value': 100000,
                'max_value': 500000,
                'criteria': {'inovação no campo': 10}
            },
            {
                'name': 'Edital Healthtech Saúde',
                'agency': 'FAPESP',
                'eligible_sectors': ['healthtech', 'biotech', 'saúde'],
                'eligible_stages': ['serie-a'],
                'min_value': 200000,
                'max_value': 1000000
            }
        ]
        return EditalMatcher(editals_data=editals)
    
    def test_match_project(self, matcher):
        """Test project matching logic"""
        description = "Startup de tecnologia para agricultura e monitoramento de safra no campo"
        matches = matcher.match_project(description)
        
        assert len(matches) > 0
        assert matches[0].name == 'Edital Agritech Inovação'
        assert float(matches[0].match_score) >= 0
    
    def test_sector_filter(self, matcher):
        """Test hard filtering by sector"""
        description = "Startup de biotech"
        
        # Should match both (both have biotech)
        matches_bio = matcher.match_project(description, sector='biotech')
        assert len(matches_bio) == 2
        
        # Should match only healthtech
        matches_health = matcher.match_project(description, sector='healthtech')
        assert len(matches_health) == 1
        assert matches_health[0].name == 'Edital Healthtech Saúde'


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests"""
    
    def test_full_pipeline(self):
        """Test complete analysis pipeline"""
        from editalshield.modules.memorial_protector import MemorialProtector
        
        # Sample memorial
        memorial = """
        Nossa startup desenvolveu o algoritmo SmartAnalyzer V3 com parâmetros 
        otimizados (W=0.85, K=2.1). Utilizamos dataset de 5M registros com 
        acurácia de 96.5%.
        
        O mercado está em expansão de 30% a.a. Nosso CAC é R$ 1500.
        """
        
        # Analyze
        protector = MemorialProtector()
        analysis = protector.analyze_memorial(memorial)
        
        # Verify analysis
        assert analysis.total_paragraphs >= 1
        assert analysis.overall_risk_score > 0
        
        # Protect
        protected, _ = protector.generate_protected_memorial(memorial)
        
        # Verify protection
        assert 'SmartAnalyzer' not in protected or '[ALGORITMO PROPRIETÁRIO]' in protected
        assert 'W=0.85' not in protected or '[PARÂMETROS OTIMIZADOS]' in protected


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
