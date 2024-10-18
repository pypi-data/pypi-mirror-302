# DSeqMap for NLP

An NLP utility for handling named entity recognition (NER) annotation data between discretized and character-wise representations. 

### Install
Use `pip install dseqmap4nlp` to install the package.

### Example
The following script demonstrates some transformation of annotation data.
```python
from dseqmap4nlp import SpacySequenceMapper, LabelLoader, CharSequenceMapper

# Load JSONL
samples = [
    {"text": "Das ist gut.", "label": [
        (0,3, "a"),
        (2,7, "b"),
        (6,8, "b")
    ]}
]

for sample in samples:
    text = sample["text"]
    anns = sample["label"]
    # Mapper @ Chars <-> SpaCy Tokens
    mapper = SpacySequenceMapper(text, nlp="de")
    # (trivial) Mapper @ Chars <-> Chars
    charmapper = CharSequenceMapper(text=text)

    # Load annotation data
    # assuming the format: [ (start_idx, stop_idx, label_class), ...]
    # and merge it with to a certain (char <-> discrete sequence) mapper
    annotationset = LabelLoader.from_text_spans(anns, mapper)
    
    # Determine number fo overlaps
    print("Overlaps:", annotationset.countOverlaps())

    # Apply the following transformations to the annotation data:
    # - transform char-based labels onto discretized sequence items (e.g. tokens)
    #   -> Expand if a label's char bounds are not exactly at token bounds
    # - Remove shorter spans in case of overlapping spans
    #   -> Note: New overlaps could also be introduced by span expansion!
    filtered_spans = annotationset\
        .toDSeqSpans(strategy=["expand"])\
        .withoutOverlaps(strategy="prefer_longest", merge_same_classes=True)

    # Check overlaps again (No overlap should exist anymore!)
    print("Overlaps:", filtered_spans.countOverlaps())

    # Transform annotation data into IOB2-formatted sequence.
    print("Sequence:")
    print(filtered_spans.toFormattedSequence(schema="IOB2"))

    # Try to generate an IOB2 sequence with overlaps. (It should fail!)
    print("Previous sequence (should fail):")
    try:
        # Should raise an error...
        print(annotationset.toFormattedSequence(schema="IOB2"))
    except ValueError as e:
        print("Error raised: " + repr(e))
```
