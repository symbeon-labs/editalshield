from pathlib import Path
from typing import Dict

class LegalKnowledgeBase:
    """
    Gerenciador da base de conhecimento jurídico e técnico (LPI, TRL, INPI).
    Carrega documentos markdown de 'docs/legal_references' para injetar no contexto do LLM.
    """

    def __init__(self, base_path: str = None):
        # Se base_path não for fornecido, assume a estrutura padrão do projeto
        if base_path:
            self.docs_path = Path(base_path)
        else:
            # Caminho relativo assumindo execução da raiz ou src
            self.docs_path = Path(__file__).parent.parent.parent.parent / "docs" / "legal_references"
        
        self.documents: Dict[str, str] = {}
        self._load_documents()

    def _load_documents(self):
        """Carrega todos os arquivos .md da pasta de referências."""
        if not self.docs_path.exists():
            print(f"⚠️ Aviso: Pasta de referência legal não encontrada: {self.docs_path}")
            return

        for file_path in self.docs_path.glob("*.md"):
            try:
                content = file_path.read_text(encoding="utf-8")
                self.documents[file_path.stem] = content
            except Exception as e:
                print(f"Erro ao carregar {file_path.name}: {e}")

    def get_context_prompt(self) -> str:
        """
        Retorna uma string formatada com todo o conhecimento legal carregado,
        pronto para ser inserido no System Prompt do Agente.
        """
        if not self.documents:
            return ""

        context_parts = ["# 📚 LEGAL KNOWLEDGE BASE & GUIDELINES\n"]
        
        # Prioridade de ordem
        priority = ["LPI_HIGHLIGHTS", "TRL_SCALE", "INPI_SOFTWARE_GUIDELINES"]
        
        # Adiciona prioritários primeiro
        for key in priority:
            if key in self.documents:
                context_parts.append(f"## {key}\n{self.documents[key]}\n")
        
        # Adiciona o restante
        for key, content in self.documents.items():
            if key not in priority:
                context_parts.append(f"## {key}\n{content}\n")

        return "\n".join(context_parts)

    def get_specific_doc(self, doc_name: str) -> str:
        """Retorna o conteúdo de um documento específico (ex: 'TRL_SCALE')."""
        return self.documents.get(doc_name, "")
