import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
    <div className="p-4 text-danger">
        <h1>Hello world!</h1>
        <App/>
    </div>
);