import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src to sys.path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from click.testing import CliRunner

from docsync.cli import improve
from docsync.core.llm import LLMResponse
from docsync.integrations.openai_provider import OpenAIProvider


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client."""
    with patch("docsync.integrations.openai_provider.OpenAI") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_openai_provider_init(mock_openai_client):
    """Test OpenAIProvider initialization."""
    provider = OpenAIProvider(api_key="test-key")
    assert provider.api_key == "test-key"
    assert provider.model == "gpt-4o-mini"


def test_openai_provider_generate(mock_openai_client):
    """Test OpenAIProvider generation."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test content"
    mock_response.usage.model_dump.return_value = {"total_tokens": 10}
    mock_openai_client.chat.completions.create.return_value = mock_response

    provider = OpenAIProvider(api_key="test-key")
    response = provider.generate("Test prompt")

    assert isinstance(response, LLMResponse)
    assert response.content == "Test content"
    assert response.usage == {"total_tokens": 10}
    
    # Verify API call
    mock_openai_client.chat.completions.create.assert_called_once()
    call_kwargs = mock_openai_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "gpt-4o-mini"
    assert len(call_kwargs["messages"]) == 1
    assert call_kwargs["messages"][0]["content"] == "Test prompt"


def test_cli_improve_command(mock_openai_client, tmp_path):
    """Test 'improve' CLI command."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Improved content"
    mock_response.usage.model_dump.return_value = {"total_tokens": 20}
    mock_openai_client.chat.completions.create.return_value = mock_response

    # Create test file
    test_file = tmp_path / "test.md"
    test_file.write_text("# Test\nContent")

    runner = CliRunner()
    
    # Mock environment variable for API key
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        result = runner.invoke(improve, [str(test_file)])

    assert result.exit_code == 0
    assert "Analyzing test.md" in result.output
    assert "Improved content" in result.output
    assert "Tokens used: 20" in result.output


def test_cli_improve_no_api_key():
    """Test 'improve' CLI command without API key."""
    runner = CliRunner()
    with patch.dict("os.environ", {}, clear=True):
        with runner.isolated_filesystem():
            with open("test.md", "w") as f:
                f.write("content")
            
            result = runner.invoke(improve, ["test.md"])
            
    assert "Configuration Error" in result.output
    assert "Set OPENAI_API_KEY" in result.output
