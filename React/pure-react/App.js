const Person = props => {
            return React.createElement('div', {}, [
                React.createElement('h1', {}, props.name),
                React.createElement('p',{}, props.occupation)
            ]);
        };

const App = () => {
            return React.createElement('div', {}, [
                React.createElement('h1', {class: 'title'}, 'React is Rendered'),
                React.createElement(Person, {name: 'Hemraj', occupation: 'Software Engineer'}, null),
                React.createElement(Person, {name: 'John', occupation: 'Data Scientist'}, null),
                React.createElement(Person, {name: 'Jane', occupation: 'Product Manager'}, null)
            ]);
        };       

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(React.createElement(App));