import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addTestimonial, addSuccessStory } from '../redux/mentalHealthSlice';

const MentalHealthDashboard = () => {
  const dispatch = useDispatch();
  // Assume the mental health slice holds the list of approved providers
  const { providers, testimonials, successStories } = useSelector(state => state.mentalHealth);

  // State for adding a patient testimonial
  const [selectedTestimonialProviderId, setSelectedTestimonialProviderId] = useState('');
  const [newTestimonialPatientName, setNewTestimonialPatientName] = useState('');
  const [newTestimonialPatientAge, setNewTestimonialPatientAge] = useState('');

  // State for adding a success story
  const [selectedSuccessStoryProviderId, setSelectedSuccessStoryProviderId] = useState('');
  const [newSuccessStoryTitle, setNewSuccessStoryTitle] = useState('');
  const [newSuccessStoryContent, setNewSuccessStoryContent] = useState('');

  // FAQ state (kept unchanged for demonstration purposes)
  const [faqOpen, setFaqOpen] = useState(null);

  const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    maxWidth: '500px',
    margin: '20px auto',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    backgroundColor: '#f9f9f9',
  };

  const inputStyle = {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '16px',
  };

  const labelStyle = {
    fontWeight: 'bold',
    marginBottom: '5px',
  };

  const buttonStyle = {
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px',
  };

  const headingStyle = {
    textAlign: 'center',
    color: '#333',
    margin: '20px 0',
  };

  const handleAddTestimonial = () => {
    if (!newTestimonialPatientName || !newTestimonialPatientAge || !selectedTestimonialProviderId) {
      alert('Please fill out all fields: patient name, age, and select a provider.');
      return;
    }

    const selectedProvider = providers.find(p => p.id === selectedTestimonialProviderId);
    if (!selectedProvider) {
      alert('Selected provider does not exist.');
      return;
    }

    if (selectedProvider.status !== 'approved') {
      alert('The selected provider has not been approved yet.');
      return;
    }

    dispatch(addTestimonial({
      providerId: selectedTestimonialProviderId,
      patientName: newTestimonialPatientName,
      patientAge: newTestimonialPatientAge,
    }));

    setNewTestimonialPatientName('');
    setNewTestimonialPatientAge('');
    alert('Testimonial added successfully!');
  };

  const handleAddSuccessStory = () => {
    if (!newSuccessStoryTitle || !newSuccessStoryContent || !selectedSuccessStoryProviderId) {
      alert('Please fill out all fields: title, content, and select a provider.');
      return;
    }

    const selectedProvider = providers.find(p => p.id === selectedSuccessStoryProviderId);
    if (!selectedProvider) {
      alert('Selected provider does not exist.');
      return;
    }

    if (selectedProvider.status !== 'approved') {
      alert('The selected provider has not been approved yet.');
      return;
    }

    dispatch(addSuccessStory({
      providerId: selectedSuccessStoryProviderId,
      title: newSuccessStoryTitle,
      content: newSuccessStoryContent,
    }));

    setNewSuccessStoryTitle('');
    setNewSuccessStoryContent('');
    alert('Success story added successfully!');
  };

  const handleFaqToggle = (index) => {
    setFaqOpen(faqOpen === index ? null : index);
  };

  return (
    <div>
      <h2 style={headingStyle}>Mental Health Dashboard</h2>

      {/* Add Patient Testimonial Form */}
      <div style={formStyle}>
        <h3>Add a Patient Testimonial</h3>
        <label style={labelStyle}>
          Select Provider:
          <select
            style={inputStyle}
            onChange={(e) => setSelectedTestimonialProviderId(e.target.value)}
            value={selectedTestimonialProviderId}
          >
            <option value="">-- Select a provider --</option>
            {providers.map(provider => (
              <option key={provider.id} value={provider.id}>{provider.name}</option>
            ))}
          </select>
        </label>

        <input
          type="text"
          style={inputStyle}
          placeholder="Patient Name"
          value={newTestimonialPatientName}
          onChange={(e) => setNewTestimonialPatientName(e.target.value)}
        />
        <input
          type="number"
          style={inputStyle}
          placeholder="Patient Age"
          value={newTestimonialPatientAge}
          onChange={(e) => setNewTestimonialPatientAge(e.target.value)}
        />
        <button style={buttonStyle} onClick={handleAddTestimonial}>Add Testimonial</button>
      </div>

      {/* Add Success Story Form */}
      <div style={formStyle}>
        <h3>Add a Success Story</h3>
        <label style={labelStyle}>
          Select Provider:
          <select
            style={inputStyle}
            onChange={(e) => setSelectedSuccessStoryProviderId(e.target.value)}
            value={selectedSuccessStoryProviderId}
          >
            <option value="">-- Select a provider --</option>
            {providers.map(provider => (
              <option key={provider.id} value={provider.id}>{provider.name}</option>
            ))}
          </select>
        </label>

        <input
          type="text"
          style={inputStyle}
          placeholder="Story Title"
          value={newSuccessStoryTitle}
          onChange={(e) => setNewSuccessStoryTitle(e.target.value)}
        />
        <textarea
          style={{ ...inputStyle, height: '100px' }}
          placeholder="Story Content"
          value={newSuccessStoryContent}
          onChange={(e) => setNewSuccessStoryContent(e.target.value)}
        />
        <button style={buttonStyle} onClick={handleAddSuccessStory}>Add Success Story</button>
      </div>

      {/* FAQ Section */}
      <div style={{ marginTop: '30px', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        <h3 style={{ marginBottom: '20px', color: '#333' }}>Frequently Asked Questions</h3>
        
        <div style={{ marginBottom: '10px' }}>
          <div
            onClick={() => handleFaqToggle(0)}
            style={{
              cursor: 'pointer',
              fontWeight: 'bold',
              color: '#007bff',
              marginBottom: '5px',
            }}
          >
            ❓ How are providers vetted?
          </div>
          {faqOpen === 0 && (
            <div style={{ paddingLeft: '20px', color: '#555' }}>
              Providers undergo a comprehensive review process where their credentials, experience, and commitment to patient care are carefully evaluated.
            </div>
          )}
        </div>
        
        <div style={{ marginBottom: '10px' }}>
          <div
            onClick={() => handleFaqToggle(1)}
            style={{
              cursor: 'pointer',
              fontWeight: 'bold',
              color: '#007bff',
              marginBottom: '5px',
            }}
          >
            ❔ Can I suggest a provider for approval?
          </div>
          {faqOpen === 1 && (
            <div style={{ paddingLeft: '20px', color: '#555' }}>
              Yes, you can recommend a provider. Please use our contact options to provide details about the provider you’d like to suggest.
            </div>
          )}
        </div>
        
        <div style={{ marginBottom: '10px' }}>
          <div
            onClick={() => handleFaqToggle(2)}
            style={{
              cursor: 'pointer',
              fontWeight: 'bold',
              color: '#007bff',
              marginBottom: '5px',
            }}
          >
            ❓ What happens if a provider doesn't meet the criteria?
          </div>
          {faqOpen === 2 && (
            <div style={{ paddingLeft: '20px', color: '#555' }}>
              If a provider fails to meet our criteria, the application will be rejected during the review process.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MentalHealthDashboard;
