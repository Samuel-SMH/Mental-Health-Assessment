import React from 'react';
import AdaptiveTest from '../components/AdaptiveTest';
import WearableIntegration from '../components/WearableIntegration';
import Telehealth from '../components/Telehealth';

const AssessmentPage = () => {
    return (
        <div className="assessment-page">
            <h1>Neuropsychological Assessment</h1>
            <AdaptiveTest />
            <WearableIntegration />
            <Telehealth />
        </div>
    );
};

export default AssessmentPage;