import React, { useEffect, useState } from 'react';

const WearableIntegration = () => {
    const [wearableData, setWearableData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchWearableData = async () => {
            try {
                // Simulate fetching data from a wearable device
                const response = await fetch('/api/wearable-data');
                if (!response.ok) {
                    throw new Error('Failed to fetch wearable data');
                }
                const data = await response.json();
                setWearableData(data);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchWearableData();
    }, []);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h2>Wearable Device Integration</h2>
            {wearableData ? (
                <div>
                    <h3>Physiological Indicators</h3>
                    <ul>
                        <li>Heart Rate: {wearableData.heartRate} bpm</li>
                        <li>Steps: {wearableData.steps}</li>
                        <li>Sleep Quality: {wearableData.sleepQuality}</li>
                    </ul>
                </div>
            ) : (
                <p>Loading wearable data...</p>
            )}
        </div>
    );
};

export default WearableIntegration;