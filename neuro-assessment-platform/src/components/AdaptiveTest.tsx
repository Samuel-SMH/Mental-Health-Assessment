import React, { useState } from 'react';

const AdaptiveTest = () => {
    const [difficulty, setDifficulty] = useState(1);
    const [score, setScore] = useState(0);
    const [questions, setQuestions] = useState([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

    const fetchQuestions = async () => {
        // Fetch questions based on the current difficulty level
        const response = await fetch(`/api/questions?difficulty=${difficulty}`);
        const data = await response.json();
        setQuestions(data);
    };

    const handleAnswer = (isCorrect) => {
        if (isCorrect) {
            setScore(score + 1);
            adjustDifficulty(true);
        } else {
            adjustDifficulty(false);
        }
        setCurrentQuestionIndex(currentQuestionIndex + 1);
    };

    const adjustDifficulty = (isCorrect) => {
        if (isCorrect && difficulty < 5) {
            setDifficulty(difficulty + 1);
        } else if (!isCorrect && difficulty > 1) {
            setDifficulty(difficulty - 1);
        }
    };

    React.useEffect(() => {
        fetchQuestions();
    }, [difficulty]);

    return (
        <div>
            <h1>Adaptive Test</h1>
            {currentQuestionIndex < questions.length ? (
                <div>
                    <h2>{questions[currentQuestionIndex].question}</h2>
                    {questions[currentQuestionIndex].answers.map((answer, index) => (
                        <button key={index} onClick={() => handleAnswer(answer.isCorrect)}>
                            {answer.text}
                        </button>
                    ))}
                </div>
            ) : (
                <div>
                    <h2>Test Complete</h2>
                    <p>Your score: {score}</p>
                </div>
            )}
        </div>
    );
};

export default AdaptiveTest;