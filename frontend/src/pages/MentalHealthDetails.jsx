import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, Link } from 'react-router-dom';
import { fetchPrograms } from '../redux/slices/programSlice';

const MentalHealthDetails = () => {
  const { programId } = useParams();
  const dispatch = useDispatch();
  const { programs, loading, error } = useSelector((state) => state.programs);
  
  useEffect(() => {
    if (!programs.length) {
      dispatch(fetchPrograms());
    }
  }, [dispatch, programs.length]);

  const program = programs.find((item) => item.id === programId);

  if (loading) {
    return <div className="text-center mt-4">Loading...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 mt-4">Error: {error}</div>;
  }

  if (!program) {
    return <div className="text-center text-gray-600 mt-4">Program not found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <section className="bg-white shadow-md rounded-lg p-6 mb-8">
          <h1 className="text-3xl font-bold text-blue-700 mb-4">{program.name}</h1>
          <p className="text-gray-700 mb-4">{program.description}</p>
          <div className="flex gap-4">
            <div className="bg-gray-100 rounded-md p-4 flex-1">
              <h3 className="text-lg font-semibold text-gray-900">Location</h3>
              <p>{program.location}</p>
            </div>
            <div className="bg-gray-100 rounded-md p-4 flex-1">
              <h3 className="text-lg font-semibold text-gray-900">Established</h3>
              <p>{program.establishedYear}</p>
            </div>
            <div className="bg-gray-100 rounded-md p-4 flex-1">
              <h3 className="text-lg font-semibold text-gray-900">Contact</h3>
              <p>{program.contactEmail}</p>
            </div>
          </div>
        </section>

        {/* Connect Call-to-Action */}
        <section className="bg-blue-700 text-white rounded-lg p-6 mb-8 text-center">
          <h2 className="text-2xl font-bold mb-2">Connect with a Doctor</h2>
          <p className="mb-4">Find the right mental health professional to support your journey.</p>
          <Link to="/doctors" className="bg-white text-blue-700 px-6 py-3 rounded-md font-semibold">
            Find a Doctor
          </Link>
        </section>

        {/* Available Doctors Section */}
        <section className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Our Doctors</h2>
          {program.doctors && program.doctors.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {program.doctors.map((doctor) => (
                <div key={doctor.id} className="bg-gray-100 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-blue-700">{doctor.name}</h3>
                  <p className="text-gray-700 mt-2">{doctor.specialty}</p>
                  <p className="text-gray-600 mt-2">{doctor.description}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-600">No doctors available</div>
          )}
        </section>
      </div>
    </div>
  );
};

export default MentalHealthDetails;
