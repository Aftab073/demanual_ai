import React, { useState } from 'react';
import './App.css'; // We will create this file next

export default function App() {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [linkedinPost, setLinkedinPost] = useState('');
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError('');
    setLinkedinPost('');

    try {
      // Fetch data from your FastAPI backend
      const response = await fetch('http://localhost:8000/generate-post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to generate post');
      }

      const data = await response.json();
      setLinkedinPost(data.linkedin_post);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-container">
      <h1>Demanual AI LinkedIn Post Generator</h1>
      <p>Enter a topic to generate a professional LinkedIn post using AI.</p>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={topic}
          onChange={e => setTopic(e.target.value)}
          placeholder="e.g., 'advancements in AI hardware'"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Post'}
        </button>
      </form>

      {error && <p className="error">Error: {error}</p>}
      
      {linkedinPost && (
        <section className="result">
          <h2>Generated LinkedIn Post</h2>
          <pre>{linkedinPost}</pre>
        </section>
      )}
    </div>
  );
}
