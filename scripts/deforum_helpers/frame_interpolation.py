from rife.inference_video import run_rife_new_video_infer

def extract_number(string):
    return int(string[1:]) if len(string) > 1 and string[1:].isdigit() else -1
        
def extract_rife_name(string):
    parts = string.split()
    if len(parts) != 2 or parts[0] != "RIFE" or (parts[1][0] != "v" or not parts[1][1:].replace('.','').isdigit()):
        raise ValueError("Input string should contain exactly 2 words, first word should be 'RIFE' and second word should start with 'v' followed by 2 numbers")
    return "RIFE"+parts[1][1:].replace('.','')

# This function usually gets a filename, and converts it to a legal linux/windows *folder* name
def clean_folder_name(string):
    illegal_chars = ["/", "\\", "<", ">", ":", "\"", "|", "?", "*"]
    for char in illegal_chars:
        string = string.replace(char, "_")
    return string
   
def process_video_interpolation(frame_interpolation_engine=None, frame_interpolation_x_amount="Disabled", frame_interpolation_slow_mo_amount="Disabled", orig_vid_fps=None, deforum_models_path=None, real_audio_track=None, raw_output_imgs_path=None, img_batch_id=None, ffmpeg_location=None, ffmpeg_crf=None, ffmpeg_preset=None, keep_interp_imgs=False, orig_vid_name=None):

    if frame_interpolation_x_amount != "Disabled":
        
        # extract clean numbers from values of 'x2' etc'
        interp_amount_clean_num = extract_number(frame_interpolation_x_amount)
        interp_slow_mo_clean_num = extract_number(frame_interpolation_slow_mo_amount)
        
        # Don't try to merge audio in the end if slow-mo is enabled
        # Todo: slow-down the music to fit the new video duraion wihout changing audio's pitch
        if real_audio_track is not None and (interp_slow_mo_clean_num != -1):
            real_audio_track = None

        # **HANDLE RIFE INTERPOLATIONS** Other models might come in the future
        if frame_interpolation_engine.startswith("RIFE"):
            # change rife model name. e.g: 'RIFE v4.3' becomes 'RIFE43' 
            actual_model_folder_name = extract_rife_name(frame_interpolation_engine)
            
            # make sure interp_amount is in its valid range
            if interp_amount_clean_num not in range(2, 11):
                raise Error("frame_interpolation_x_amount must be between 2x and 10x")
            
            # set initial output vid fps
            fps = float(orig_vid_fps) * interp_amount_clean_num
            # re-calculate fps param to pass if slow_mo mode is enabled
            if interp_slow_mo_clean_num != -1:
                if int(interp_slow_mo_clean_num) not in [2,4,8]:
                    raise Error("frame_interpolation_slow_mo_amount must be 2x, 4x or 8x")
                fps = float(orig_vid_fps) * int(interp_amount_clean_num) / int(interp_slow_mo_clean_num)
                
            # run actual interpolation and video stitching etc - the whole suite
            if actual_model_folder_name:
                run_rife_new_video_infer(interp_x_amount=interp_amount_clean_num, slow_mo_x_amount=interp_slow_mo_clean_num, output=None, model=actual_model_folder_name, fps=fps, deforum_models_path=deforum_models_path, audio_track=real_audio_track, raw_output_imgs_path=raw_output_imgs_path, img_batch_id=img_batch_id, ffmpeg_location=ffmpeg_location, ffmpeg_crf=ffmpeg_crf, ffmpeg_preset=ffmpeg_preset, keep_imgs=keep_interp_imgs, orig_vid_name=orig_vid_name)          
