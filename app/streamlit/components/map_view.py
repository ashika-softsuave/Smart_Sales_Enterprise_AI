import streamlit as st
import streamlit.components.v1 as components


def render_map(encoded_polyline: str):
    html = f"""
    <html>
      <head>
         <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCzT9oC-kt40CKOdYBvUQC_k59AD0oLpbs&libraries=geometry"></script>
      </head>
      <body>
        <div id="map" style="height:500px;"></div>
        <script>
          function initMap(){{
            var map=new google.maps.Map(document.getElementById('map'),{{
              zoom:12,
              center:{{lat:12.8996,lng:80.2209}}
            }});

            var path=google.maps.geometry.encoding.decodePath("{encoded_polyline}");

            new google.aps.Polyline({{
              path:path,
              geodesic:true,
              strokeOpacity:1.0,
              strokeWeight:4
            }}).setMap(map;
          }}
          initMap();
        </script>
       </body>
       </html> 
       """
    components.html(html, height=550)