import React, { Component } from 'react';

import Map from './components/Map.jsx';


const fetchPlaces = (f) => {
  fetch('/place_data/').then((response) => {
    // Convert to JSON
    return response.json();
  }).then((data) => {
    f(data);
  });
};


export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = { places: false };
  }

  get_data() {
    fetchPlaces((data) => this.setState({ places: data }));
  }

  componentDidMount() {
    this.get_data();
  }

  render() {
    return (
      <div id="map">
        <Map places={this.state.places}/>
      </div>
    );
  }
}
