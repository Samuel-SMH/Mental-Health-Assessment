import React, { useState } from 'react';

const Telehealth: React.FC = () => {
    const [appointmentDate, setAppointmentDate] = useState('');
    const [appointmentTime, setAppointmentTime] = useState('');
    const [neuropsychologist, setNeuropsychologist] = useState('');
    const [confirmationMessage, setConfirmationMessage] = useState('');

    const handleScheduleAppointment = () => {
        // Logic to schedule the appointment with the selected neuropsychologist
        setConfirmationMessage(`Appointment scheduled with ${neuropsychologist} on ${appointmentDate} at ${appointmentTime}.`);
    };

    return (
        <div className="telehealth-container">
            <h2>Telehealth Consultations</h2>
            <div>
                <label>
                    Select Neuropsychologist:
                    <select value={neuropsychologist} onChange={(e) => setNeuropsychologist(e.target.value)}>
                        <option value="">Select...</option>
                        <option value="Dr. Smith">Dr. Smith</option>
                        <option value="Dr. Johnson">Dr. Johnson</option>
                        <option value="Dr. Lee">Dr. Lee</option>
                    </select>
                </label>
            </div>
            <div>
                <label>
                    Appointment Date:
                    <input type="date" value={appointmentDate} onChange={(e) => setAppointmentDate(e.target.value)} />
                </label>
            </div>
            <div>
                <label>
                    Appointment Time:
                    <input type="time" value={appointmentTime} onChange={(e) => setAppointmentTime(e.target.value)} />
                </label>
            </div>
            <button onClick={handleScheduleAppointment}>Schedule Appointment</button>
            {confirmationMessage && <p>{confirmationMessage}</p>}
        </div>
    );
};

export default Telehealth;