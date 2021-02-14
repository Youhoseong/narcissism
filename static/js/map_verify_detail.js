

          var container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
          var options = { //지도를 생성할 때 필요한 기본 옵션
            center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
            level: 3 // 지도의 확대 레벨 
          };

          var map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
          var gpsPosition;
          var clickLine;
          var distanceval;
          map.setZoomable(false); 
          map.setDraggable(false); 


          updatebtn = document.getElementById('btn-yes');
          updatebtn.style.display = "none";
                    
            // HTML5의 geolocation으로 사용할 수 있는지 확인합니다 
            if (navigator.geolocation) {
                
                // GeoLocation을 이용해서 접속 위치를 얻어옵니다
                navigator.geolocation.getCurrentPosition(function(position) {
                    
                    var lat = position.coords.latitude, // 위도
                        lon = position.coords.longitude; // 경도
                    
                    var locPosition = new kakao.maps.LatLng(lat, lon), // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다
                        message = '<div class="title" style="padding:5px;">여기에 계신가요?!</div>'; // 인포윈도우에 표시될 내용입니다
                    
                    gpsPosition = locPosition;
                    // 마커와 인포윈도우를 표시합니다
                    displayMarker(locPosition, message);
                        
                });
                
            } else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
                
                var locPosition = new kakao.maps.LatLng(33.450701, 126.570667),    
                    message = 'geolocation을 사용할수 없어요..'
                    
                displayMarker(locPosition, message);
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
                searchAddrFromCoords(map.getCenter(), displayCenterInfo);   
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

                  for(var i = 0; i < result.length; i++) {
                      // 행정동의 region_type 값은 'H' 이므로
                      if (result[i].region_type === 'H') {
                           infoDiv.innerHTML = result[i].address_name;
                           temp = result[i].address_name;
                           break;
                      }
                  }
              }    
          }

          function deleteClickLine() {
            if (clickLine) {
                clickLine.setMap(null);    
                clickLine = null;        
            }
        }

          var submitbut = document.getElementById('msg');

          submitbut.onkeydown = function(event){
              if(event.keyCode == 13) {
                    var locationform = document.getElementById('msg');
                
                    geocoder.addressSearch(locationform.value, function(result, status) {

                        // 정상적으로 검색이 완료됐으면 
                        if (status === kakao.maps.services.Status.OK) {
                            console.log('wow');
                            var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                    
                            // 결과값으로 받은 위치를 마커로 표시합니다
                            var marker = new kakao.maps.Marker({
                                map: map,
                                position: coords
                            });
                    
                            // 인포윈도우로 장소에 대한 설명을 표시합니다
                            var infowindow = new kakao.maps.InfoWindow({
                                content: '<div style="width:150px;text-align:center;padding:6px 0;">검색결과</div>'
                            });
                            infowindow.open(map, marker);
                            console.log(coords);
                            // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
                            map.setCenter(coords);
                            

                        
                            console.log(gpsPosition);

                
                            clickLine = new kakao.maps.Polyline({
                                map: map, // 선을 표시할 지도입니다 
                                path: [coords, gpsPosition], // 선을 구성하는 좌표 배열입니다 클릭한 위치를 넣어줍니다
                                strokeWeight: 3, // 선의 두께입니다 
                                strokeColor: '#db4040', // 선의 색깔입니다
                                strokeOpacity: 1, // 선의 불투명도입니다 0에서 1 사이값이며 0에 가까울수록 투명합니다
                                strokeStyle: 'solid' // 선의 스타일입니다
                            });

                            distanceval = Math.round(clickLine.getLength());
                            if(distanceval > 5000) {
                                negativemsg = '<div class="text-red-400">주소 인증 불가</div>';
                                reasonmsg = '<div class="font-light">GPS 기반 주소로 부터 너무 떨어져있습니다.</div>' ;
                                msg = document.getElementById('warningmsg');
                                msg2 = document.getElementById('reasonmsg');
                      
                                msg.innerHTML = negativemsg; 
                                msg2.innerHTML = reasonmsg;
                               
                                updatebtn = document.getElementById('btn-yes');
                                updatebtn.style.display = "none";
                            
                            }
                            else {
                                negativemsg = '<div class="text-green-600">주소 인증이 가능합니다.</div>';
                                msg = document.getElementById('warningmsg');
                                msg.innerHTML = negativemsg; 

                                updatebtn = document.getElementById('btn-yes');
                                updatebtn.style.display = "block";
                                document.getElementById('reasonmsg').style.display="none";
                                
                            }
                          

                            console.log(distanceval);
                            deleteClickLine();
                        } 
                        else {
                            console.log('tq');
                        }
                    });       
        }
        } 
        
            $(document).ready(function(){
                $('#btn-yes').click(function(){
                    if(distanceval <= 5000) {
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
                    }
                    else {
                        test = 'GPS 기반 주소로 부터 5km 이하의 거리만 사용자가 수정할 수 있습니다.';
                        msg = document.getElementById(warningmsg);
                        msg.innerHTML = test;       
                    }
                });
            });
       
