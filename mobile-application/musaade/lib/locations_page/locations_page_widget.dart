import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:localstorage/localstorage.dart';

import '../activity_page/activity_page_widget.dart';
import '../components/location_item_widget.dart';
import '../flutter_flow/flutter_flow_theme.dart';
import '../flutter_flow/flutter_flow_util.dart';

class LocationsPageWidget extends StatefulWidget {
  const LocationsPageWidget({Key key}) : super(key: key);

  @override
  _LocationsPageWidgetState createState() => _LocationsPageWidgetState();
}

class _LocationsPageWidgetState extends State<LocationsPageWidget> {
  LocalStorage sessionStorage = LocalStorage("session_data");
  List locationList;

  Future<String> getLocations() async {
    String token = sessionStorage.getItem('token');
    String baseURL = sessionStorage.getItem('baseURL');
    String locationURL = baseURL + "/api/location/";
    try {
      HttpClient client = new HttpClient();
      client.badCertificateCallback =
          ((X509Certificate cert, String host, int port) => true);

      HttpClientRequest request = await client.getUrl(Uri.parse(locationURL));
      request.headers.set("Authorization", "token $token");
      HttpClientResponse response = await request.close();

      var data = json.decode(await response.transform(utf8.decoder).join());

      this.setState(() {
        locationList = data;
      });

      // print(locationList);
      return "Updated!";
    } catch (e) {
      locationList = [];
      showDialog(
          context: context,
          builder: (context) {
            Future.delayed(Duration(seconds: 2), () {
              Navigator.of(context).pop(true);
            });
            return AlertDialog(
              title: Text(
                'Cannot connect to server!',
                style: FlutterFlowTheme.bodyText1.override(
                  fontFamily: 'Poppins',
                  color: FlutterFlowTheme.primaryColor,
                ),
              ),
            );
          });
      return "Failed!";
    }
  }

  Future<void> refreshLocations() {
    this.getLocations();
    return Future.delayed(Duration(seconds: 0));
  }

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    this.getLocations();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: scaffoldKey,
      backgroundColor: FlutterFlowTheme.secondaryColor,
      body: SafeArea(
        child: Align(
          alignment: AlignmentDirectional(0, 0),
          child: Container(
            width: double.infinity,
            height: double.infinity,
            decoration: BoxDecoration(
              color: FlutterFlowTheme.secondaryColor,
            ),
            child: Column(
              mainAxisSize: MainAxisSize.max,
              children: [
                Align(
                  alignment: AlignmentDirectional(0, 0),
                  child: Container(
                    width: double.infinity,
                    height: 60,
                    decoration: BoxDecoration(
                      color: FlutterFlowTheme.primary,
                    ),
                    child: Padding(
                      padding: EdgeInsetsDirectional.fromSTEB(20, 0, 20, 1),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text(
                            'Locations',
                            style: FlutterFlowTheme.title1.override(
                              fontFamily: 'Poppins',
                              color: FlutterFlowTheme.secondaryColor,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
                Expanded(
                  child: Padding(
                    padding: EdgeInsetsDirectional.fromSTEB(20, 20, 20, 0),
                    child: RefreshIndicator(
                        color: FlutterFlowTheme.primary,
                        onRefresh: refreshLocations,
                        child: ListView.builder(
                          itemCount:
                              locationList == null ? 0 : locationList.length,
                          itemBuilder: (BuildContext context, int index) {
                            return new InkWell(
                              onTap: () async {
                                await Navigator.push(
                                  context,
                                  PageTransition(
                                    type: PageTransitionType.rightToLeft,
                                    duration: Duration(milliseconds: 300),
                                    reverseDuration:
                                        Duration(milliseconds: 300),
                                    child: ActivityPageWidget(
                                      locationName: locationList[index]["name"],
                                      locationID: locationList[index]["id"],
                                    ),
                                  ),
                                );
                              },
                              child: LocationItemWidget(
                                locationName: locationList[index]["name"],
                              ),
                            );
                          },
                        )),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
