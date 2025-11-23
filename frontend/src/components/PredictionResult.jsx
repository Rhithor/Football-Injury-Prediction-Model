import './PredictionResult.css'

const PredictionResult = ({ result }) => {
  if (result.error) {
    return (
      <div className="prediction-result error">
        <h2>Error</h2>
        <p>{result.message || result.error}</p>
      </div>
    )
  }

  const riskLevel = result.injury_risk
  const riskClass = riskLevel === 'high' ? 'high-risk' : 'low-risk'
  const riskPercentage = (result.risk_probability * 100).toFixed(1)

  return (
    <div className={`prediction-result ${riskClass}`}>
      <h2>Prediction Result</h2>
      
      <div className="risk-indicator">
        <div className={`risk-badge ${riskClass}`}>
          <span className="risk-label">Injury Risk:</span>
          <span className="risk-value">{riskLevel.toUpperCase()}</span>
        </div>
        <div className="risk-percentage">
          {riskPercentage}% probability
        </div>
      </div>

      {result.recommendations && result.recommendations.length > 0 && (
        <div className="recommendations">
          <h3>Recommendations</h3>
          <ul>
            {result.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default PredictionResult

