import os
import fnmatch


def find_pictures_without_prefixes(directory, include_subdirectories=False):
    matches = []
    patterns = ['*.jpg', '*.jpeg', '*.png', '*.gif']  # Add more patterns if needed

    if include_subdirectories:
        for root, dirs, files in os.walk(directory):
            for pattern in patterns:
                for filename in fnmatch.filter(files, pattern):
                    if not ("C-" in filename or "im-" in filename):
                        matches.append(os.path.join(root, filename))
    else:
        for pattern in patterns:
            for filename in fnmatch.filter(os.listdir(directory), pattern):
                if not ("C-" in filename or "im-" in filename):
                    matches.append(os.path.join(directory, filename))

    return matches
