# report
intent_report(A, Facts) :- exec(Facts), store(output_type('report'), output_report(A)).
