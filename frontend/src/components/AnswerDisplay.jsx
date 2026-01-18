function AnswerDisplay({ answer }) {
    return (
      <div className="answer-display">
        <div className="answer-header">
          <h2>Answer</h2>
          {answer.routing && (
            <div className="routing-info">
              <span className="badge badge-type">{answer.routing.type}</span>
              {answer.routing.sections && answer.routing.sections.length > 0 && (
                <span className="badge badge-section">
                  {answer.routing.sections.join(', ')}
                </span>
              )}
              {answer.routing.confidence && (
                <span className="badge badge-confidence">
                  {Math.round(answer.routing.confidence * 100)}% confidence
                </span>
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