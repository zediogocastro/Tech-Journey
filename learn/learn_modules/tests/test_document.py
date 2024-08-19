import sys
sys.path.append("/workspaces/Tech-Journey/learn/learn_modules/")

from text_analyzer import Document

print("Hello!")

def test_document_tokens():
    doc = Document('a e i o u')

    assert doc.tokens == ['a', 'e', 'i', 'o', 'u']