import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignInPage.css';

const SignInPage = () => {
    const [username, setUsername] = useState('');
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [allUsernames, setAllUsernames] = useState([]);
    const [msg, setMsg] = useState('');
    const [showCreatePopup, setShowCreatePopup] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        fetch('http://localhost:5000/all_users')
            .then(res => res.json())
            .then(data => {
                setAllUsernames(data.usernames || []);
            })
            .catch(err => console.error("Failed to fetch usernames", err));
    }, []);

    const handleInputChange = (e) => {
        const value = e.target.value;
        setUsername(value);
        setMsg('');

        const matches = allUsernames.filter(u =>
            u.toLowerCase().includes(value.toLowerCase())
        );

        if (
            matches.length === 0 ||
            matches.some(u => u.toLowerCase() === value.toLowerCase())
        ) {
            setShowSuggestions(false);  // hide if exact match or no matches
        } else {
            setShowSuggestions(true);   // show if still some partial matches
        }
    };


    const handleSignIn = (e) => {
        e.preventDefault();
        fetch('http://localhost:5000/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username }),
        })
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            return response.json();
        })
        .then(data => {
            console.log('Sign in successful:', data);
            sessionStorage.setItem('username', username);
            navigate('/');
        })
        .catch(async error => {
            const errMsg = await error.json();
            console.error('Error signing in:', errMsg);
            if (errMsg.error === 'User not found') {
                setShowCreatePopup(true);
            } else {
                setMsg('An error occurred. Please try again.');
            }
        });
    };

    const createNewUser = () => {
        fetch('http://localhost:5000/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username })
        })
        .then(res => res.json())
        .then(data => {
            console.log("User created", data);
            sessionStorage.setItem('username', username);
            navigate('/');
        })
        .catch(err => {
            console.error("Error creating user", err);
            setMsg("Failed to create user.");
        })
        .finally(() => setShowCreatePopup(false));
    };

    const filteredSuggestions = username
        ? allUsernames.filter(u => u.toLowerCase().includes(username.toLowerCase()))
        : [];

    return (
        <div className="container">
            <h1>Sign In</h1>
            <form onSubmit={handleSignIn}>
                <div className="input-wrapper">
                    <label htmlFor="username">Username:</label>
                    <input
                    type="text"
                    id="username"
                    value={username}
                    onChange={handleInputChange}
                    required
                    autoComplete="off"
                    />
                    {showSuggestions && filteredSuggestions.length > 0 && (
                    <div className="suggestion-box">
                        {filteredSuggestions.map((u, i) => (
                        <div
                            key={i}
                            className="suggestion-item"
                            onClick={() => {
                            setUsername(u);
                            setShowSuggestions(false);
                            }}
                        >
                            {u}
                        </div>
                        ))}
                    </div>
                    )}
                </div>

                {/* This button will now always be pushed down */}
                <button type="submit">Sign In</button>
                </form>


            {showCreatePopup && (
                <div className="popup">
                    <div className="popup-content">
                        <p>Username <strong>{username}</strong> not found.<br />Create a new user?</p>
                        <button onClick={createNewUser}>Yes</button>
                        <button onClick={() => setShowCreatePopup(false)}>Cancel</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SignInPage;
