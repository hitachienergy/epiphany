import React, { Component } from 'react';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {state: 'redirecting', token: null, data1: null, data2: null};
  }

  xhr( method, url, headers, callback ) {
    const xhr = new XMLHttpRequest();
    xhr.open( method, window.location.origin + url );
    xhr.onreadystatechange = function() {
        if ( xhr.readyState === 4 ) {
            callback( xhr );
        }
    };
    xhr.setRequestHeader('Accept', 'application/json');
    for(let i = 0; i < headers.length; i++) {
      const header = headers[i];
      xhr.setRequestHeader(header.id, header.value);
    }   
    xhr.send();
  };

  loadData(path, key){
    const t = this;
    let state = {};
    this.xhr('GET',
        path,
        [{
          "id" : "Authorization", 
          "value"   : 'Bearer ' + t.state.token
        }],
        (response) => {
          if (response.status === 200) {
            state[key] =  response.responseText;
            t.setState(state);
          } else if (response.status === 403) {
            state[key] =  'Forbidden';
            t.setState(state);
          }
        }
    );
  }

  login = () => {
    window.location.href = window.location.origin + '/login';
  }     

  logout = () => {
    window.location.href = window.location.origin + '/logout';
  }    

  componentDidMount() {
    const t = this;
    this.xhr('GET',
        '/state',
        [],
        (response) => {
           if (response.status === 200) {
             if(JSON.parse(response.responseText).authenticated){
                t.setState({state: 'authenticated'});
             } else {
                t.setState({state: 'not-authenticated'});
             }
             t.setState({authenticated: JSON.parse(response.responseText).authenticated});
             if(t.state.state === 'authenticated') {
                this.xhr('GET',
                  '/token',
                  [],
                  (response) => {
                    if (response.status === 200) {
                      t.setState({token: JSON.parse(response.responseText).token});
                      this.loadData('/api/Values/1', 'data1');
                      this.loadData('/api/Values', 'data2');            
                    }
                  }
                );
             }     
           }
         }
    );
  }  

  render() {
    if (this.state.state === 'authenticated' ) {
      return (
        <div>
          <p><b>Authenticated!</b></p>
          <button onClick={this.logout}>Logout</button>
          <p><b>Token:</b></p>
          <textarea value={this.state.token} rows="8" cols="75" />   
          <p><b>Result of user service call (api/Values/id):</b></p>
          <textarea value={this.state.data1} rows="8" cols="75" />   
          <p><b>Result of administrator service call (api/Values):</b></p>
          <textarea value={this.state.data2} rows="8" cols="75" />                  
        </div>
      )
    } else if (this.state.state === 'not-authenticated' ) {
      return (
        <div>
          <p><b>Welcom! Click below to login</b></p>
          <button onClick={this.login}>Login</button>
        </div>
      )
    } else if (this.state.state === 'redirecting' ) {
      return (<div>
        <p><b>Redirecting...</b></p>
      </div>)
    }
  }
}
export default App;