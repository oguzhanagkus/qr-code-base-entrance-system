import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:localstorage/localstorage.dart';

import '../flutter_flow/flutter_flow_theme.dart';

class ActivityPageWidget extends StatefulWidget {
  const ActivityPageWidget({Key key, this.locationName, this.locationID})
      : super(key: key);

  final String locationName;
  final int locationID;

  @override
  _ActivityPageWidgetState createState() => _ActivityPageWidgetState();
}

class _ActivityPageWidgetState extends State<ActivityPageWidget> {
  final scaffoldKey = GlobalKey<ScaffoldState>();

  LocalStorage sessionStorage = LocalStorage("session_data");
  String info = "No activity.";
  IconData icon = FontAwesomeIcons.infoCircle;
  Color color = FlutterFlowTheme.primary;

  void pollActivity() async {
    if (this.mounted) {
      print("--");
      String token = sessionStorage.getItem('token');
      String baseURL = sessionStorage.getItem('baseURL');
      String locationURL = baseURL + "/api/activity/";
      print(locationURL);
      try {
        Map map = {
          'id': widget.locationID,
        };

        HttpClient client = new HttpClient();
        client.badCertificateCallback =
            ((X509Certificate cert, String host, int port) => true);

        HttpClientRequest request =
            await client.postUrl(Uri.parse(locationURL));
        request.headers.set("Authorization", "token $token");
        request.add(utf8.encode(json.encode(map)));
        HttpClientResponse response = await request.close();

        var data =
            json.decode(await response.transform(utf8.decoder).join()) as Map;
        print(data);
        if (data.containsKey('result')) {
          setState(() {
            if (data.containsKey('personnel')) {
              info = data["personnel"];
            } else {
              info = data["first_name"] + " " + data["last_name"];
            }
            if (data['result'] == true) {
              icon = FontAwesomeIcons.solidCheckCircle;
              color = FlutterFlowTheme.success;
            } else {
              icon = FontAwesomeIcons.solidTimesCircle;
              color = FlutterFlowTheme.danger;
            }
          });
        }
        changeDefault();
      } catch (e) {
        print(e);
      }
    }
  }

  void changeDefault() async {
    try {
      if (this.mounted) {
        await Future.delayed(Duration(seconds: 2));
        this.setState(() {
          info = "No activity!";
          icon = FontAwesomeIcons.infoCircle;
          color = FlutterFlowTheme.primary;
        });
      }
    } catch (e) {
      print(e);
    }
  }

  void initState() {
    super.initState();
    Timer.periodic(Duration(seconds: 5), (_) => pollActivity());
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
                  child: Padding(
                    padding: EdgeInsetsDirectional.fromSTEB(0, 0, 0, 10),
                    child: Container(
                      width: double.infinity,
                      height: 60,
                      decoration: BoxDecoration(
                        color: FlutterFlowTheme.primary,
                      ),
                      child: Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(20, 0, 20, 0),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Text(
                              widget.locationName,
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
                ),
                Align(
                  alignment: AlignmentDirectional(0, 0),
                  child: Container(
                    width: double.infinity,
                    height: MediaQuery.of(context).size.height * 0.5,
                    decoration: BoxDecoration(),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        FaIcon(
                          icon,
                          color: color,
                          size: 100,
                        ),
                        Text(
                          info,
                          style: FlutterFlowTheme.title2,
                        )
                      ],
                    ),
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
