import { useState } from 'react'
import './PredictionForm.css'

const PredictionForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    age: '',
    matches_played: '',
    minutes_played: '',
    previous_injuries: '',
    fatigue_level: '0.5',
    training_load: '0.5',
    recovery_time: '48',
    position: 'midfielder',
    fitness_score: '0.8',
    weather_condition: 'normal'
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // normalize types
    const submitData = {
      ...formData,
      age: parseInt(formData.age),
      matches_played: parseInt(formData.matches_played),
      minutes_played: parseInt(formData.minutes_played),
      previous_injuries: parseInt(formData.previous_injuries),
      fatigue_level: parseFloat(formData.fatigue_level),
      training_load: parseFloat(formData.training_load),
      recovery_time: parseInt(formData.recovery_time),
      fitness_score: parseFloat(formData.fitness_score),
    }
    
    onSubmit(submitData)
  }

  return (
    <form className="prediction-form" onSubmit={handleSubmit}>
      <h2>Player Information</h2>
      
      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="age">Age</label>
          <input
            type="number"
            id="age"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
            min="16"
            max="45"
          />
        </div>

        <div className="form-group">
          <label htmlFor="position">Position</label>
          <select
            id="position"
            name="position"
            value={formData.position}
            onChange={handleChange}
            required
          >
            <option value="goalkeeper">Goalkeeper</option>
            <option value="defender">Defender</option>
            <option value="midfielder">Midfielder</option>
            <option value="forward">Forward</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="matches_played">Matches Played (this season)</label>
          <input
            type="number"
            id="matches_played"
            name="matches_played"
            value={formData.matches_played}
            onChange={handleChange}
            required
            min="0"
          />
        </div>

        <div className="form-group">
          <label htmlFor="minutes_played">Total Minutes Played</label>
          <input
            type="number"
            id="minutes_played"
            name="minutes_played"
            value={formData.minutes_played}
            onChange={handleChange}
            required
            min="0"
          />
        </div>

        <div className="form-group">
          <label htmlFor="previous_injuries">Previous Injuries (count)</label>
          <input
            type="number"
            id="previous_injuries"
            name="previous_injuries"
            value={formData.previous_injuries}
            onChange={handleChange}
            required
            min="0"
          />
        </div>

        <div className="form-group">
          <label htmlFor="recovery_time">Recovery Time (hours since last match)</label>
          <input
            type="number"
            id="recovery_time"
            name="recovery_time"
            value={formData.recovery_time}
            onChange={handleChange}
            required
            min="0"
          />
        </div>

        <div className="form-group">
          <label htmlFor="fatigue_level">Fatigue Level (0-1)</label>
          <input
            type="range"
            id="fatigue_level"
            name="fatigue_level"
            value={formData.fatigue_level}
            onChange={handleChange}
            min="0"
            max="1"
            step="0.1"
          />
          <span className="range-value">{formData.fatigue_level}</span>
        </div>

        <div className="form-group">
          <label htmlFor="training_load">Training Load (0-1)</label>
          <input
            type="range"
            id="training_load"
            name="training_load"
            value={formData.training_load}
            onChange={handleChange}
            min="0"
            max="1"
            step="0.1"
          />
          <span className="range-value">{formData.training_load}</span>
        </div>

        <div className="form-group">
          <label htmlFor="fitness_score">Fitness Score (0-1)</label>
          <input
            type="range"
            id="fitness_score"
            name="fitness_score"
            value={formData.fitness_score}
            onChange={handleChange}
            min="0"
            max="1"
            step="0.05"
          />
          <span className="range-value">{formData.fitness_score}</span>
        </div>

        <div className="form-group">
          <label htmlFor="weather_condition">Weather Condition</label>
          <select
            id="weather_condition"
            name="weather_condition"
            value={formData.weather_condition}
            onChange={handleChange}
            required
          >
            <option value="normal">Normal</option>
            <option value="hot">Hot</option>
            <option value="cold">Cold</option>
            <option value="wet">Wet</option>
          </select>
        </div>
      </div>

      <button type="submit" className="submit-button" disabled={loading}>
        {loading ? 'Predicting...' : 'Predict Injury Risk'}
      </button>
    </form>
  )
}

export default PredictionForm

