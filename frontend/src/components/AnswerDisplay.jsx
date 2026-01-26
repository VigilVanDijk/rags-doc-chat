function AnswerDisplay({ answer, verboseToggle }) {
  return (
    <div className="answer-display">
      <div className="answer-header">
        <h2>Answer</h2>
        {answer.routing && verboseToggle && (
          <div className="routing-info">
            <div className="badge-wrapper">
              <span className="badge badge-type">{answer.routing.query_type}</span>
              <span className="tooltip">The type of query detected by the routing system</span>
            </div>
            {answer.routing.sections && answer.routing.sections.length > 0 && (
              <div className="badge-wrapper">
                <span className="badge badge-section">
                  {answer.routing.sections.join(', ')}
                </span>
                <span className="tooltip">Document sections used to generate this answer</span>
              </div>
            )}
            {answer.routing.confidence && (
              <div className="badge-wrapper">
                <span className="badge badge-confidence">
                  {Math.round(answer.routing.confidence * 100)}%
                </span>
                <span className="tooltip">Confidence score of the query routing decision</span>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="answer-query">
        <strong>Q:</strong> {answer.query}
      </div>

      <div className="answer-content">
        {answer.answer}
      </div>
    </div>
  )
}

export default AnswerDisplay