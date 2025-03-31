import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { setProviderDetails } from '../redux/providersSlice';

const ProviderApplication = () => {
  const [providerName, setProviderName] = useState('');
  const [providerDescription, setProviderDescription] = useState('');
  const [yearsOfExperience, setYearsOfExperience] = useState('');
  const [faqOpen, setFaqOpen] = useState(null);
  const dispatch = useDispatch();

  const handleApply = () => {
    if (!providerName || !providerDescription || !yearsOfExperience) {
      alert('Please fill out all fields.');
      return;
    }

    dispatch(setProviderDetails({
      name: providerName,
      description: providerDescription,
      experience: yearsOfExperience,
      status: 'pending', // Mark as pending until admin approval
    }));
    alert('Provider application submitted!');
  };

  const handleFaqToggle = (index) => {
    setFaqOpen(faqOpen === index ? null : index);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h2 style={{ marginBottom: '20px', color: '#333' }}>Apply to Become a Mental Health Provider</h2>
      
      <input
        type="text"
        placeholder="Provider Name"
        value={providerName}
        onChange={(e) => setProviderName(e.target.value)}
        style={{
          width: '100%',
          marginBottom: '10px',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '5px',
        }}
      />
      
      <textarea
        placeholder="Provider Description"
        value={providerDescription}
        onChange={(e) => setProviderDescription(e.target.value)}
        style={{
          width: '100%',
          marginBottom: '10px',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '5px',
          resize: 'none',
        }}
      />
      
      <input
        type="number"
        placeholder="Years of Experience"
        value={yearsOfExperience}
        onChange={(e) => setYearsOfExperience(e.target.value)}
        style={{
          width: '100%',
          marginBottom: '20px',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '5px',
        }}
      />
      
      <button
        onClick={handleApply}
        style={{
          padding: '10px 20px',
          backgroundColor: '#28a745',
          color: '#fff',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        Submit Application
      </button>

      {/* FAQ Section */}
      <div style={{ marginTop: '30px' }}>
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
              Yes, you can recommend a provider. Please use the contact options on our platform to provide details about the provider you’d like to suggest.
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

export default ProviderApplication;
