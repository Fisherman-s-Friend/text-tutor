import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignInPage.css';

const SignInPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [msg, setMsg] = useState('');
    const navigate = useNavigate();

    // Reset the message when the user starts typing in either username or email field
    const handleInputChange = () => {
        setMsg('');
    };


    const handleSignIn = (e) => {
        e.preventDefault();
        console.log('Sign in:', { username, email });
        // Send a request to the server to verify the credentials for sign-in
        fetch('http://localhost:5000/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Sign in successful:', data);
            // Handle successful sign-in (e.g., redirect to another page)
            sessionStorage.setItem('username', username);
            navigate('/');
        })
        .catch(error => {
            console.error('Error signing in:', error);
            setMsg('An error occurred while signing in. Please try again.');
        });
    };

    return (
        <div className='container'>
            <h1>Sign In/Sign Up Page</h1>
            <form onSubmit={handleSignIn}>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => { setUsername(e.target.value); handleInputChange(); }}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => { setEmail(e.target.value); handleInputChange(); }}
                        required
                    />
                </div>
                <button type="submit">Sign In/Up</button>
                {msg && <p>{msg}</p>}
            </form>
        </div>
    );
};

export default SignInPage;
