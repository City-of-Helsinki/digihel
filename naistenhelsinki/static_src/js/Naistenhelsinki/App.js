import React, { Component } from 'react';

import { Map, Marker, Popup, TileLayer} from 'react-leaflet';

import * as L from 'leaflet';

function numberIcon (content) {
    return L.divIcon({
        className: "number-icon",
        iconSize: [21, 21],
        iconAnchor: [10, 44],
        popupAnchor: [3, -40],
        html: content});
}

function createMarkup() {
    return {__html: 'First &middot; Second'};
}

function Content(props) {
    return <div dangerouslySetInnerHTML={{__html: props.content}} />;
}

class OneMap extends Component {

  render() {
    const position = [60.172059, 24.945831]; // Default to Helsinki's center
    const bounds = [
      [59.9, 24.59],  // SouthWest corner
      [60.43, 25.3]  // NorthEast corner
    ];

    const places = this.props.places;
    if (places) {
        let markers = places.features.map((feature, index) => {

            if (!feature.geometry) return null;

            let icon = numberIcon(index + 1);

            return (
                <Marker key={feature.properties.name} position={feature.geometry.coordinates.reverse()} icon={icon}>
                    <Popup>
                        <Content content={feature.properties.description} />
                    </Popup>
                </Marker>
            );
        });

        return (
            <Map center={position} zoom={13}>
                <TileLayer
                    url='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    minZoom={10} maxZoom={16} zoomControl={true}
                />
                {markers}
            </Map>
        );
    } else {
        return null;
    }
  }
}

/*
<FeatureGroup
  ref={(input) => {
    if (!input) return;
    const bounds = input.leafletElement.getBounds();
    if (bounds.isValid()) {
      input.props.map.fitBounds(bounds);
      const viewportBounds = [
        [59.9, 24.59],  // SouthWest corner
        [60.43, 25.3]  // NorthEast corner
      ];  // Wide Bounds of City of Helsinki area
      input.props.map.setMaxBounds(viewportBounds);
    }
  }}
>{contents}</FeatureGroup>
*/


const fetch_places = (f) => {
    fetch('/place_data/').then(function(response) {
        // Convert to JSON
        return response.json();
    }).then(function(data) {
        console.log("data arrived", data);
        f(data);
    });
};


class App extends Component {
    constructor(props) {
        super(props);
        this.state = {places: false};
    }

    get_data() {
        fetch_places(data => this.setState({places: data}));
    }

    componentDidMount() {
        this.get_data();
    }

    render() {
        return (
          <div id="map">
            <OneMap places={this.state.places} />
          </div>
        );
    }
}

export default App;