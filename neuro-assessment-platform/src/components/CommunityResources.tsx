import React from 'react';

const CommunityResources: React.FC = () => {
    const resources = [
        {
            title: 'Local Support Group',
            description: 'Join our weekly support group for individuals facing neuropsychological challenges.',
            link: 'https://example.com/support-group'
        },
        {
            title: 'Cognitive Workshops',
            description: 'Participate in workshops designed to enhance cognitive skills and provide coping strategies.',
            link: 'https://example.com/cognitive-workshops'
        },
        {
            title: 'Online Resources',
            description: 'Access a variety of online materials and videos to learn more about neuropsychological conditions.',
            link: 'https://example.com/online-resources'
        }
    ];

    return (
        <div className="community-resources">
            <h2>Community Resources</h2>
            <ul>
                {resources.map((resource, index) => (
                    <li key={index}>
                        <h3>{resource.title}</h3>
                        <p>{resource.description}</p>
                        <a href={resource.link} target="_blank" rel="noopener noreferrer">Learn More</a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CommunityResources;