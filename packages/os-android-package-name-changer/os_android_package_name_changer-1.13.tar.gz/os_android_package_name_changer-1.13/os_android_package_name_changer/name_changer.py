import os
import os_tools.logger_handler as lh
import os_xml_handler.xml_handler as xh
import os_file_handler.file_handler as fh
import os
import re
from os_android_package_name_changer.bp import _name_changer_boilerplate as bp
###########################################################################
#
# this module meant to substitute old android package name with a new one
#   Arguments:
#   1) android project path (String)
#   2) new package name (String)
#
###########################################################################


def change_package_name(project_path, new_package_name):
    # setup the logger
    logger = lh.Logger(__file__)

    # get the old package name
    old_package_name = get_package_name(project_path)

    logger.info("checking write permission in directory")
    # check if write permission granted
    bp.check_write_permission(project_path)

    logger.info("changing package name")
    # change the package name
    bp.change_package_name(project_path, old_package_name, new_package_name)

    logger.info("changing 3 inner dirs (inside src/main)")
    # change the 3 inner folders inside the src/main (/GeneralRemote/app/src/main/java/com/first/second)
    bp.change_inner_folders_names(project_path, old_package_name, new_package_name)

    logger.info("changing settings.gradle rootProject.name")
    # change the 3 inner folders inside the src/main (/GeneralRemote/app/src/main/java/com/first/second)
    bp.change_settings_gradle_file(project_path, new_package_name)

    logger.info("done!")


# will return a package name from a given project from the build gradle
def get_package_name(project_path):

    app_dir = os.path.join(project_path, 'app')
    gradle_file = os.path.join(app_dir, 'build.gradle')

    package_name = None

    try:
        with open(gradle_file, 'r') as file:
            for line in file:
                # First, check for namespace
                namespace_match = re.search(r'namespace\s+\'([\w\.]+)\'', line)
                if namespace_match:
                    package_name = namespace_match.group(1)
                    break

            # If no namespace found, check for applicationId
            if not package_name:
                file.seek(0)  # Reset file pointer to the beginning to search again
                for line in file:
                    app_id_match = re.search(r'applicationId\s+"([\w\.]+)"', line)
                    if app_id_match:
                        package_name = app_id_match.group(1)
                        break
    except FileNotFoundError:
        print(f"build.gradle not found in {gradle_file}")

    return package_name
