import React, { Component } from 'react';
import Keycloak from 'keycloak-js';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { keycloak: null, data1: null, data2: null };
  }

  login() {
    this.state.keycloak.init({onLoad: 'login-required'})
    .success(() => { 
      this.loadData('/api/Values/1', 'data1');
      this.loadData('/api/Values', 'data2');
      this.forceUpdate();
    });
  }

  logout = () => {
    this.state.keycloak.logout()
    .success(() => { 
      this.forceUpdate();
    });
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
          "value"   : 'Bearer ' + t.state.keycloak.token
        }],
        (response) => {
          if (response.status === 200) {
            state[key] =  response.responseText;
            t.setState(state);
          } else if (response.status === 403) {

            state[key] = 'Forbidden';
            t.setState(state);
          }
        }
    );
  }

  componentDidMount() {
    const t = this;
    let state = {};       
    this.xhr('GET',
        '/config',
        [],
        (response) => {
          if (response.status === 200) {
            state.keycloak = Keycloak(JSON.parse(response.responseText));
            t.setState(state);     
            this.login();    
          }
        }
    );
  }  

  render() {
    if (this.state.keycloak !== null && this.state.keycloak.authenticated) {
      return (
        <div>
          <p><b>Authenticated!</b></p>
          <button onClick={this.logout}>Logout</button>
          <p><b>Token:</b></p>
          <textarea value={this.state.keycloak.token} rows="8" cols="75" />   
          <p><b>Result of user service call (api/Values/id):</b></p>
          <textarea value={this.state.data1} rows="8" cols="75" />   
          <p><b>Result of administrator service call (api/Values):</b></p>
          <textarea value={this.state.data2} rows="8" cols="75" />                  
        </div>
      )
    } else {
      return (
        <div>
          Redirecting...
        </div>
      )
    }
  }
}
export default App;