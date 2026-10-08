def create_image_password(images):
    return ",".join(images)


def check_image_password(saved_password, selected_images):
    current_password = ",".join(selected_images)

    if saved_password == current_password:
        return True
    else:
        return False