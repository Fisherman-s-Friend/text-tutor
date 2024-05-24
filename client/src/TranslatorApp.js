import React, { useState, useRef, useEffect } from 'react';
import './TranslatorApp.css';
import LanguageSelect from './LanguageSelect'; // Import the LanguageSelect component
import Tooltip from './Tooltip'; // Import the Tooltip component
import languages from './stanza_languages'; // Import the languages object
import googleTransLanguages from './googleTrans_languages';
//import { useNavigate } from 'react-router-dom';

const TranslatorApp = () => {

    // (1) Define variables and states ------------------>
    const [inputText, setInputText] = useState('');
    const [translatedText, setTranslatedText] = useState('');
    const [definitions, setDefinitions] = useState('');
    const [tokens, setTokens] = useState([]); // State to store the tokens
    const [synonyms, setSynonyms] = useState('');
    const [Rephrase, setRephrase] = useState(''); // Add this line
    const [selectedText, setSelectedText] = useState('');
    const [selectedTextVisible, setSelectedTextVisible] = useState(false);
    const [selectionStart, setSelectionStart] = useState(0);
    const [selectionEnd, setSelectionEnd] = useState(0);
    const [contextMenuVisible, setContextMenuVisible] = useState(false);
    const [contextMenuPosition, setContextMenuPosition] = useState({ top: 0, left: 0 });
    const [outputBoxVisible, setOutputBoxVisible] = useState(false);
    const [loading, setLoading] = useState(false);
    const [selectedLanguage, setSelectedLanguage] = useState('en');
    const [inputLanguage, setInputLanguage] = useState('en');
    const inputRef = useRef(null);
    const loggedInUsername = sessionStorage.getItem('username');
    const [pastRequests, setPastRequests] = useState([]);
    const [selectedRequest, setSelectedRequest] = useState("");
    //const navigate = useNavigate();
    // -------------------------------------------------||

    const fetchUserRequests = () => {
      setLoading(true);
      fetch(`http://localhost:5000/requests/${loggedInUsername}`, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          },
      })
      .then(response => response.json())
      .then(data => {
          setPastRequests(data.requests);
      })
      .catch(error => {
          console.error('Error:', error);
      })
      .finally(() => {
          setLoading(false);
      });
    };
  
  


    // (2) Define functions ----------------------------->
    const handleInputChange = (e) => {
        setInputText(e.target.value);
      };
    
      useEffect(() => {
        setTranslatedText('');
        setDefinitions('');
        setSynonyms('');
        setRephrase(''); // Add this line
      }, [selectedText]);
    
      const handleActions = (text, action) => {
        setLoading(true);
        const selectedTextChanged = text !== selectedText;
        fetch('http://localhost:5000/api', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text, action, language: selectedLanguage, inputLanguage, selectionStart, selectionEnd}),
        })
          .then(response => response.json())
          .then(data => {
            if (selectedTextChanged) {
              // Update all states if selectedText has changed
              setTranslatedText(data.translation);
              setDefinitions(data.definitions);
              setSynonyms(data.synonyms);
              setRephrase(data.Rephrase); // Add this line
            }
            else {
              // Update only non-empty states if selectedText has not changed
              if (data.translation) setTranslatedText(data.translation);
              if (data.definitions) setDefinitions(data.definitions);
              if (data.synonyms) setSynonyms(data.synonyms);
              if (data.Rephrase) setRephrase(data.Rephrase); // Add this line
            }
          })
          .catch(error => console.error('Error:', error))
          .finally(() => {
            setLoading(false);
          });
      };
      
      const handleMouseUp = (e) => {
        const textarea = e.target;
        const selectionStart = textarea.selectionStart;
        const selectionEnd = textarea.selectionEnd;
      
        const selectedText = textarea.value.substring(selectionStart, selectionEnd);
      
        setSelectionStart(selectionStart);
        setSelectionEnd(selectionEnd);
        
        setSelectedText(selectedText);
      
        // Show context menu if text is selected
        if (selectedText.trim() !== '') {
          setContextMenuVisible(true);
          // Calculate context menu position based on mouse coordinates
          setContextMenuPosition({ top: e.clientY, left: e.clientX });
        } else {
          setContextMenuVisible(false);
        }
      };
      
    
      const handleActionsContextMenu = (action) => {
        handleActions(selectedText, action);
        setSelectedTextVisible(true);
        //setContextMenuVisible(false);
      };
    
      const handleLanguageChange = (e) => {
        setSelectedLanguage(e.target.value);
      };
    
      const handleInputLanguageChange = (e) => {
        setInputLanguage(e.target.value);
      };
    
      const sendTokenInfo = (tokens) => {
        fetch('http://localhost:5000/tokens', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputText, language: selectedLanguage, inputLanguage, username: loggedInUsername, tokens}),
        })
        .catch(error => {
            console.error('Error:', error);
        }); 
    };
    

    const fetchLanguageForRequest = (selectedValue) => {
      // Fetch the request data from the server
      fetch(`http://localhost:5000/request/${selectedValue}`, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          },
      })
      .then(response => response.json())
      .then(data => {
          setInputLanguage(data.language); // Update input language with language from the selected request
          setTokens(data.extra_data); // Set tokens with the extra data from the selected request
          setOutputBoxVisible(true);
        })
      .catch(error => {
          console.error('Error:', error);
      });
  };
  


    const handleSubmit = () => {
    setLoading(true);
    setSelectedTextVisible(false);
    fetch('http://localhost:5000/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText, language: selectedLanguage, inputLanguage, username: loggedInUsername}),
    })
    .then(response => response.json())
    .then(data => {
        setTokens(data); // Set the tokens state with the response data
        sendTokenInfo(data);
        setOutputBoxVisible(true);
        fetchUserRequests(); // Update the history
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        setLoading(false);
    });
    };

    return (
        <div className="translator-container">
           {loggedInUsername && (
            <div className='Box'>You're logged in as {loggedInUsername}
            <div>
              <div className="history-controls translator-controls">
                <select value={selectedRequest} onChange={(e) => {
                    setSelectedRequest(e.target.value);
                    setInputText(e.target.value); // Update the input text with the selected request
                    fetchLanguageForRequest(e.target.value); // Fetch language and extra data for the selected request
                }}>
                    <option value="">Select a past request...</option>
                    {pastRequests.map(request => (
                        <option key={request.id} value={request.data}>
                            {request.data.substring(0, 20) + "..."}
                        </option>
                    ))}
                </select>
                <button className="history-button" onClick={fetchUserRequests}>
                    Update History
                </button>
            </div>
          </div>
        </div>
        )}
  
          <textarea
            ref={inputRef}
            className="input-textarea"
            value={inputText}
            onChange={handleInputChange}
            onMouseUp={handleMouseUp}
            placeholder="Enter text to process..."
          />
          <div className="translator-controls">
            <LanguageSelect
              label="Text Input Language"
              value={inputLanguage}
              onChange={handleInputLanguageChange}
              languages={languages}
            />
            <LanguageSelect
              label="Translation Output Language"
              value={selectedLanguage}
              onChange={handleLanguageChange}
              languages={googleTransLanguages}
              className="custom-width"
            />
            <button className="translate-button" onClick={() => {handleSubmit(inputText); handleActions(inputText, "submit")}}>
              Submit
            </button>
          </div>
          {outputBoxVisible &&
          <div id="tokensContainer" className="tokensContainer">
        {tokens.map((token, index) => (
            <Tooltip key={index} content={
            <div>
                <div className="tooltip-attribute">Lemma: {token.lemma}</div>
                <div className="tooltip-attribute">Morphology: {token.morphology}</div>
                <div className="tooltip-attribute">POS: {token.POS}</div>
                <div className="tooltip-attribute">DEP: {token.DEP}</div>
                <div className="tooltip-attribute">Head: {token.head}</div>
                <div className="tooltip-attribute">Definition: {token.definitions}</div>
            </div>
            }>
            <span className="token-span" id={`token-${index + 1}`} text={token.text}>
                {token.text}
            </span>
            </Tooltip>
        ))}
        </div>}
          {loading && <p className="loading-box">Loading...</p>}
          {selectedTextVisible && <p className="selected-text-label">Selected Text: {selectedText}</p>}
          <div className="translated-text-container">
            <div className="translated-box">
              <p className="translated-text-label">Translation:</p>
              <p className="translated-text">{translatedText}</p>
            </div>
            <div className="translated-box">
              <p className="definitions-label">Definitions:</p>
              <p className="definitions">{definitions}</p>
            </div>
            <div className="translated-box">
              <p className="synonyms-label">Synonyms:</p>
              <p className="synonyms">{synonyms}</p>
            </div>
            <div className="translated-box">
              <p className="Rephrase-label">Rephrase:</p>
              <p className="Rephrase">{Rephrase}</p>
            </div>
          </div>
    
    
          {contextMenuVisible && (
            <div
              className="context-menu"
              style={{
                top: contextMenuPosition.top,
                left: contextMenuPosition.left,
              }}
            >
              <button onMouseEnter={() => handleActionsContextMenu("translate")}>Translate</button>
              <button onMouseEnter={() => handleActionsContextMenu("define")}>Define</button>
              <button onMouseEnter={() => handleActionsContextMenu("synonyms")}>Synonyms</button>
              <button onMouseEnter={() => handleActionsContextMenu("Rephrase")}>Rephrase</button>
              <button onMouseEnter={() => setContextMenuVisible(false)}>Hide</button>
            </div>
          )}
        </div>
      );
    };

export default TranslatorApp;