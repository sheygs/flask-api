import { useState } from 'react';

function App() {
        const [count, setCount] = useState(0);

        return (
                <>
                        <p>Hello, React {count}!</p>
                        <button
                                className="btn btn-primary"
                                onClick={() => setCount((count) => count + 1)}
                        >
                                count is {count}
                        </button>
                </>
        );
}

export default App;
