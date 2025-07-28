import React from 'react';
import { Link } from 'react-router-dom';
import './styles/main.css';

const HomePage: React.FC = () => {
    return (
        <div className="homepage">
            <h1>Welcome to the Neuropsychological Assessment Platform</h1>
            <p>
                Our innovative solution leverages cutting-edge technologies to provide a comprehensive neuropsychological assessment tool.
            </p>
            <nav>
                <ul>
                    <li>
                        <Link to="/assessment">Start Assessment</Link>
                    </li>
                    <li>
                        <Link to="/telehealth">Telehealth Consultations</Link>
                    </li>
                    <li>
                        <Link to="/community">Community Resources</Link>
                    </li>
                </ul>
            </nav>
        </div>
    );
};

export default HomePage;