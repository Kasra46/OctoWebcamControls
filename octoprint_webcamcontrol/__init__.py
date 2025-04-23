import octoprint.plugin
import flask
import paramiko
import json
import os

class WebcamControlPlugin(octoprint.plugin.SettingsPlugin,
                         octoprint.plugin.AssetPlugin,
                         octoprint.plugin.TemplatePlugin,
                         octoprint.plugin.BlueprintPlugin):

    def get_settings_defaults(self):
        return dict(
            hostname="",
            username="",
            password="",
            port=22
        )

    def get_assets(self):
        return dict(
            js=["js/webcamcontrol.js"],
            css=["css/webcamcontrol.css"]
        )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False),
            dict(type="tab", custom_bindings=False)
        ]

    def get_ssh_connection(self):
        settings = self._settings.get_all_data()
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=settings["hostname"],
                username=settings["username"],
                password=settings["password"],
                port=settings["port"]
            )
            return ssh, None
        except Exception as e:
            return None, str(e)

    def execute_ssh_command(self, command):
        ssh, error = self.get_ssh_connection()
        if error:
            return None, error

        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if error and "no process found" not in error.lower():
                return None, error
            
            return output, None
        except Exception as e:
            return None, str(e)
        finally:
            if ssh:
                ssh.close()

    @octoprint.plugin.BlueprintPlugin.route("/execute", methods=["POST"])
    def execute_command(self):
        output, error = self.execute_ssh_command('bash webcamfhd.sh')
        if error:
            return flask.jsonify(error=error), 500
        return flask.jsonify(success=True, output=output)

    @octoprint.plugin.BlueprintPlugin.route("/endstream", methods=["POST"])
    def end_stream(self):
        output, error = self.execute_ssh_command('pkill mjpg_streamer')
        if error:
            return flask.jsonify(error=error), 500
        return flask.jsonify(success=True, output=output)

    @octoprint.plugin.BlueprintPlugin.route("/restartv4l2", methods=["POST"])
    def restart_v4l2(self):
        commands = [
            'pkill mjpg_streamer',
            'modprobe -r uvcvideo',
            'modprobe uvcvideo'
        ]
        
        for command in commands:
            output, error = self.execute_ssh_command(command)
            if error:
                return flask.jsonify(error=error), 500
        
        return flask.jsonify(success=True, output='v4l2 restarted successfully')

    @octoprint.plugin.BlueprintPlugin.route("/fhd", methods=["POST"])
    def fhd_quality(self):
        output, error = self.execute_ssh_command('./webcamfhd.sh')
        if error:
            return flask.jsonify(error=error), 500
        return flask.jsonify(success=True, output=output)

    @octoprint.plugin.BlueprintPlugin.route("/qhd", methods=["POST"])
    def qhd_quality(self):
        output, error = self.execute_ssh_command('./webcamqhd.sh')
        if error:
            return flask.jsonify(error=error), 500
        return flask.jsonify(success=True, output=output)

    @octoprint.plugin.BlueprintPlugin.route("/quality960", methods=["POST"])
    def quality_960(self):
        output, error = self.execute_ssh_command('./webcam960.sh')
        if error:
            return flask.jsonify(error=error), 500
        return flask.jsonify(success=True, output=output)

    @octoprint.plugin.BlueprintPlugin.route("/webcamconfig", methods=["POST"])
    def webcam_config(self):
        output, error = self.execute_ssh_command('./webcamconfig.sh')
        if error:
            return flask.jsonify(error=error), 500
        return flask.jsonify(success=True, output=output)

__plugin_name__ = "Webcam Control"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = WebcamControlPlugin() 