import operator

def show_features(model, text=None, n=15):
    #take vectorizer and classifier from the pipeline
    vectorizer = model.named_steps['vectorizer']
    classifier = model.named_steps['classifier']

    if text is not None:
        # Compute coef_ for input
        verbose_text_features = model.transform([text]).toarray()
    else:
        # Otherwise use coef_ itself
        verbose_text_features = classifier.coef_

    #zip the feature names with the coefs and sort
    coefs = sorted(
        zip(verbose_text_features[0], vectorizer.get_feature_names()),
        key=operator.itemgetter(0), reverse=True
    )

    # Get the top and bottom coefs in name pairs
    important_features = zip(coefs[:n], coefs[:-(n+1):-1])

    # Create two columns with most negative and most positive features.
    output = []
    for (positive_coef, positive_feature), (negative_coef, negative_feature) in important_features:
        output.append(
            "{:0.4f}{: >15}    {:0.4f}{: >15}".format(
                positive_coef, positive_feature, negative_coef, negative_feature
            )
        )

    return "\n".join(output)