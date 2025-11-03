'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

interface Flashcard {
  id: number;
  front_text: string;
  back_text: string;
  order_index: number;
}

interface FlashcardDeck {
  id: number;
  title: string;
  description: string;
  card_count: number;
  cards: Flashcard[];
  created_at: string;
}

export default function FlashcardsPage() {
  const { user } = useAuth();
  const [decks, setDecks] = useState<FlashcardDeck[]>([]);
  const [selectedDeck, setSelectedDeck] = useState<FlashcardDeck | null>(null);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Form states
  const [showCreateDeck, setShowCreateDeck] = useState(false);
  const [showAddCard, setShowAddCard] = useState(false);
  const [deckTitle, setDeckTitle] = useState('');
  const [deckDescription, setDeckDescription] = useState('');
  const [frontText, setFrontText] = useState('');
  const [backText, setBackText] = useState('');

  useEffect(() => {
    if (user) {
      loadDecks();
    }
  }, [user]);

  const loadDecks = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8009/api/flashcards/decks/user/${user?.id || 1}`);
      if (response.ok) {
        const data = await response.json();
        setDecks(data);
      }
    } catch (err) {
      setError('Failed to load decks');
    } finally {
      setLoading(false);
    }
  };

  const createDeck = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8009/api/flashcards/decks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user?.id || 1,
          title: deckTitle,
          description: deckDescription
        })
      });
      
      if (response.ok) {
        setDeckTitle('');
        setDeckDescription('');
        setShowCreateDeck(false);
        await loadDecks();
      }
    } catch (err) {
      setError('Failed to create deck');
    } finally {
      setLoading(false);
    }
  };

  const addCard = async () => {
    if (!selectedDeck) return;
    
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8009/api/flashcards/cards', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          deck_id: selectedDeck.id,
          front_text: frontText,
          back_text: backText
        })
      });
      
      if (response.ok) {
        setFrontText('');
        setBackText('');
        setShowAddCard(false);
        // Reload the selected deck
        const deckResponse = await fetch(`http://localhost:8009/api/flashcards/decks/${selectedDeck.id}`);
        if (deckResponse.ok) {
          const updatedDeck = await deckResponse.json();
          setSelectedDeck(updatedDeck);
          await loadDecks();
        }
      }
    } catch (err) {
      setError('Failed to add card');
    } finally {
      setLoading(false);
    }
  };

  const reviewCard = async (quality: number) => {
    if (!selectedDeck || !selectedDeck.cards[currentCardIndex]) return;
    
    try {
      await fetch('http://localhost:8009/api/flashcards/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          card_id: selectedDeck.cards[currentCardIndex].id,
          user_id: user?.id || 1,
          quality
        })
      });
      
      // Move to next card
      if (currentCardIndex < selectedDeck.cards.length - 1) {
        setCurrentCardIndex(currentCardIndex + 1);
        setShowAnswer(false);
      }
    } catch (err) {
      setError('Failed to record review');
    }
  };

  const currentCard = selectedDeck?.cards[currentCardIndex];

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Flashcards</h1>
        <p className="text-gray-600 mt-2">Study with spaced repetition</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {!selectedDeck ? (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Your Decks</h2>
            <button
              onClick={() => setShowCreateDeck(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Create New Deck
            </button>
          </div>

          {showCreateDeck && (
            <div className="bg-white p-6 rounded-lg shadow mb-6">
              <h3 className="text-lg font-semibold mb-4">Create Flashcard Deck</h3>
              <input
                type="text"
                placeholder="Deck Title"
                value={deckTitle}
                onChange={(e) => setDeckTitle(e.target.value)}
                className="w-full px-4 py-2 border rounded mb-3"
              />
              <textarea
                placeholder="Description (optional)"
                value={deckDescription}
                onChange={(e) => setDeckDescription(e.target.value)}
                className="w-full px-4 py-2 border rounded mb-3"
                rows={3}
              />
              <div className="flex gap-2">
                <button
                  onClick={createDeck}
                  disabled={!deckTitle || loading}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-300"
                >
                  Create
                </button>
                <button
                  onClick={() => setShowCreateDeck(false)}
                  className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {decks.map((deck) => (
              <div
                key={deck.id}
                onClick={() => setSelectedDeck(deck)}
                className="bg-white p-6 rounded-lg shadow hover:shadow-lg cursor-pointer transition"
              >
                <h3 className="text-lg font-semibold mb-2">{deck.title}</h3>
                <p className="text-gray-600 text-sm mb-3">{deck.description}</p>
                <div className="text-sm text-gray-500">
                  {deck.card_count} cards
                </div>
              </div>
            ))}
          </div>

          {decks.length === 0 && !loading && (
            <div className="text-center py-12 text-gray-500">
              No flashcard decks yet. Create one to get started!
            </div>
          )}
        </div>
      ) : (
        <div>
          <div className="flex justify-between items-center mb-6">
            <div>
              <button
                onClick={() => {
                  setSelectedDeck(null);
                  setCurrentCardIndex(0);
                  setShowAnswer(false);
                }}
                className="text-blue-600 hover:text-blue-700 mb-2"
              >
                ← Back to Decks
              </button>
              <h2 className="text-2xl font-bold">{selectedDeck.title}</h2>
              <p className="text-gray-600">{selectedDeck.description}</p>
            </div>
            <button
              onClick={() => setShowAddCard(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Add Card
            </button>
          </div>

          {showAddCard && (
            <div className="bg-white p-6 rounded-lg shadow mb-6">
              <h3 className="text-lg font-semibold mb-4">Add Flashcard</h3>
              <textarea
                placeholder="Front (Question)"
                value={frontText}
                onChange={(e) => setFrontText(e.target.value)}
                className="w-full px-4 py-2 border rounded mb-3"
                rows={3}
              />
              <textarea
                placeholder="Back (Answer)"
                value={backText}
                onChange={(e) => setBackText(e.target.value)}
                className="w-full px-4 py-2 border rounded mb-3"
                rows={3}
              />
              <div className="flex gap-2">
                <button
                  onClick={addCard}
                  disabled={!frontText || !backText || loading}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-300"
                >
                  Add Card
                </button>
                <button
                  onClick={() => setShowAddCard(false)}
                  className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {currentCard ? (
            <div className="max-w-2xl mx-auto">
              <div className="text-center mb-4 text-gray-600">
                Card {currentCardIndex + 1} of {selectedDeck.cards.length}
              </div>

              <div
                onClick={() => setShowAnswer(!showAnswer)}
                className="bg-white p-12 rounded-lg shadow-lg cursor-pointer hover:shadow-xl transition min-h-[300px] flex items-center justify-center"
              >
                <div className="text-center">
                  <div className="text-2xl font-semibold mb-4">
                    {showAnswer ? currentCard.back_text : currentCard.front_text}
                  </div>
                  <div className="text-sm text-gray-500">
                    {showAnswer ? 'Click to see question' : 'Click to reveal answer'}
                  </div>
                </div>
              </div>

              {showAnswer && (
                <div className="mt-6">
                  <p className="text-center text-gray-700 mb-4">How well did you know this?</p>
                  <div className="flex justify-center gap-2">
                    <button
                      onClick={() => reviewCard(1)}
                      className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                    >
                      Again
                    </button>
                    <button
                      onClick={() => reviewCard(3)}
                      className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
                    >
                      Hard
                    </button>
                    <button
                      onClick={() => reviewCard(4)}
                      className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                    >
                      Good
                    </button>
                    <button
                      onClick={() => reviewCard(5)}
                      className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    >
                      Easy
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              No cards in this deck yet. Add some cards to start studying!
            </div>
          )}
        </div>
      )}
    </div>
  );
}
