var container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
          var options = { //지도를 생성할 때 필요한 기본 옵션
            center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
            level: 1 // 지도의 확대 레벨 
          };

          var map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
          var temp_lat = 0;
          var temp_lon = 0;
                    
            // HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
            if (navigator.geolocation) {
                
                // GeoLocation을 이용해서 접속 위치를 얻어옵니다
                navigator.geolocation.getCurrentPosition(function(position) {
                    
                    var lat = position.coords.latitude, // 위도
                        lon = position.coords.longitude; // 경도
                    
                    temp_lat = lat;
                    temp_lon = lon;
                    
                    var locPosition = new kakao.maps.LatLng(lat, lon), // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
                        message = '<div class="title" style="padding:5px;">여기에 계신가요?!</div>'; // 인포윈도우에 표시될 내용입니다
                    
                    // 마커와 인포윈도우를 표시합니다
                    displayMarker(locPosition, message);
                        
                });
                
            } else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
                
                var locPosition = new kakao.maps.LatLng(33.450701, 126.570667),    
                    message = 'geolocation을 사용할수 없어요..'
                    
                displayMarker(locPosition, message);
            }
            setDraggable(false); //드래그 불가하게 설정

            function setDraggable(draggable) {
                // 마우스 드래그로 지도 이동 가능여부를 설정합니다
                map.setDraggable(draggable);    
            }

            // 지도에 마커와 인포윈도우를 표시하는 함수입니다
            function displayMarker(locPosition, message) {

                // 마커를 생성합니다
                var marker = new kakao.maps.Marker({  
                    map: map, 
                    position: locPosition
                }); 
                
                var iwContent = message, // 인포윈도우에 표시할 내용
                    iwRemoveable = true;

                // 인포윈도우를 생성합니다
                var infowindow = new kakao.maps.InfoWindow({
                    content : iwContent,
                    removable : iwRemoveable
                });
                
                // 인포윈도우를 마커위에 표시합니다 
                infowindow.open(map, marker);
                
                // 지도 중심좌표를 접속위치로 변경합니다
                map.setCenter(locPosition);    
                map.setLevel(3)  
            }    

            // 주소-좌표 변환 객체를 생성합니다
          var geocoder = new kakao.maps.services.Geocoder();
          // 현재 지도 중심좌표로 주소를 검색해서 지도 좌측 상단에 표시합니다
          searchAddrFromCoords(map.getCenter(), displayCenterInfo);   
          
          kakao.maps.event.addListener(map, 'idle', function() {
            searchAddrFromCoords(map.getCenter(), displayCenterInfo);
          });

          function searchAddrFromCoords(coords, callback) {
              // 좌표로 행정동 주소 정보를 요청합니다
              geocoder.coord2RegionCode(coords.getLng(), coords.getLat(), callback);         
          }

          function searchDetailAddrFromCoords(coords, callback) {
              // 좌표로 법정동 상세 주소 정보를 요청합니다
              geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
          }

          // 지도 좌측상단에 지도 중심좌표에 대한 주소정보를 표출하는 함수입니다
          var temp="";
          function displayCenterInfo(result, status) {
              if (status === kakao.maps.services.Status.OK) {
                  var infoDiv = document.getElementById('centerAddr');
                  var infoDiv2 = document.getElementById('loc');

                  for(var i = 0; i < result.length; i++) {
                      // 행정동의 region_type 값은 'H' 이므로
                      if (result[i].region_type === 'H') {
                           infoDiv.innerHTML = result[i].address_name;
                           infoDiv2.innerHTML = result[i].address_name;
                           temp = result[i].address_name;
                          break;
                      }
                  }
              }    
          }

          $(document).ready(function(){
                $('#btn-yes').click(function(){
                        $.ajax({
                            type: "POST",
                            url: verify_complete_url,
                            data: {
                                "location": temp,
                                'csrfmiddlewaretoken': '{{ csrf_token }}'
                            },
                            dataType: "json",
                            async: false,
                            success: function (data) {
                                // any process in data
                                alert("successfull")
                            },
                            failure: function () {
                                alert("failure");
                            }
                        });
                });



                
            });
          
                $('#btn-no').click(function(){
                        $.ajax({
                            type: "POST",
                            url: verify_detail_url,
                            data: {
                                "lat": temp_lat,
                                "lon": temp_lon,
                                'csrfmiddlewaretoken': '{{ csrf_token }}'
                            },
                            dataType: "json",
                            async: false,
                            success: function (data) {
                                // any process in data
                                alert("successfull")
                            },
                            failure: function () {
                                alert("failure");
                            }
                        });
                });
            
