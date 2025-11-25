import { useState } from 'react'
import PredictionForm from './PredictionForm'
import PredictionResult from './PredictionResult'
import '../App.css'

const Home = () => {
  const [predictionResult, setPredictionResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handlePrediction = async (formData) => {
    setLoading(true)
    setPredictionResult(null)

    try {
      const response = await fetch('http://localhost:8000/api/predict/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error('Prediction failed')
      }

      const data = await response.json()
      setPredictionResult(data)
    } catch (error) {
      setPredictionResult({
        error: error.message,
        message: 'Failed to get prediction. Please check if the backend is running.'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>⚽ Football Injury Prediction</h1>
          <p>Predict injury risk for football players using AI</p>
        </div>
      </header>

      <main className="App-main">
        <div className="container">
          <PredictionForm onSubmit={handlePrediction} loading={loading} />
          {predictionResult && <PredictionResult result={predictionResult} />}
        </div>
      </main>
    </div>
  )
}

export default Home

