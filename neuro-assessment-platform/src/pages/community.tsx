import React from 'react';
import CommunityResources from '../components/CommunityResources';

const CommunityPage: React.FC = () => {
    return (
        <div>
            <h1>Community Engagement</h1>
            <p>Welcome to our community resources page. Here you can find information about local workshops, support groups, and other resources available to you.</p>
            <CommunityResources />
        </div>
    );
};

export default CommunityPage;