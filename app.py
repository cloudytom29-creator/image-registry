import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import segno
import base64
import io

# ==========================================
# PAGE CONFIGURATION & SETUP
# ==========================================
st.set_page_config(
    page_title="Creative Engine Studio", 
    page_icon="⚡", 
    layout="wide"
)

# Helper function to compute image file size metrics in KB
def get_image_bytes_size(img, format_str="PNG", quality=100):
    try:
        buf = io.BytesIO()
        if format_str.upper() in ["JPEG", "JPG"]:
            img.save(buf, format=format_str, quality=quality)
        else:
            img.save(buf, format=format_str)
        return len(buf.getvalue()) / 1024.0
    except Exception:
        return 0.0

# ==========================================
# WORKSPACE NAVIGATION
# ==========================================
st.sidebar.title("🚀 Navigation Center")
workspace_mode = st.sidebar.radio(
    "Select Environment Workflow:",
    ["🎨 Advanced Image Studio", "🔮 Universal QR Engine"]
)

st.sidebar.markdown("---")

# ==========================================
# MODE A: ADVANCED IMAGE STUDIO
# ==========================================
if workspace_mode == "🎨 Advanced Image Studio":
    st.title("🎨 Advanced Image Studio")
    st.write("Apply dynamic visual layers, manipulate boundaries, and inspect live asset size optimization metrics.")
    
    uploaded_file = st.file_uploader("Upload Canvas Source Image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # Load raw asset
            original_image = Image.open(uploaded_file)
            width, height = original_image.size
            
            # Workspace Architecture Columns
            control_col, display_col = st.columns([1, 2])
            
            with control_col:
                st.subheader("⚙️ Modification Engines")
                
                # --- FILTER SELECTION ---
                st.markdown("### 1. High-Fidelity Filters")
                selected_filter = st.selectbox(
                    "Choose Creative Mask:",
                    [
                        "Original", "Black & White", "Sepia Tone", "Gaussian Blur", 
                        "Contour Sketch", "Vibrant Saturation", "Retro Negative", "Emboss Art"
                    ]
                )
                
                # --- CANVAS MANIPULATION ---
                st.markdown("### 2. Direct Canvas Tools")
                
                # Resize Tool
                with st.expander("📐 Scale & Dimension Resizing"):
                    maintain_aspect = st.checkbox("Lock Aspect Ratio", value=True)
                    if maintain_aspect:
                        new_width = st.number_input("Target Width (Pixels):", min_value=1, max_value=10000, value=int(width))
                        scale_factor = new_width / float(width)
                        new_height = int(height * scale_factor)
                        st.caption(f"Calculated Lock Height: **{new_height} px**")
                    else:
                        new_width = st.number_input("Target Width (Pixels):", min_value=1, max_value=10000, value=int(width))
                        new_height = st.number_input("Target Height (Pixels):", min_value=1, max_value=10000, value=int(height))
                
                # Crop Tool
                with st.expander("✂️ Pixel Boundary Cropping"):
                    st.caption("Slice borders inward relative to canvas margins.")
                    crop_left = st.slider("Crop Left Margin", 0, int(width // 2), 0)
                    crop_right = st.slider("Crop Right Margin", 0, int(width // 2), 0)
                    crop_top = st.slider("Crop Top Margin", 0, int(height // 2), 0)
                    crop_bottom = st.slider("Crop Bottom Margin", 0, int(height // 2), 0)
                
                # Compression Engine
                st.markdown("### 3. Compression Controls")
                compression_quality = st.slider("Target Save Quality", 1, 100, 85)
                export_format = st.selectbox("Output Formatting Target:", ["PNG", "JPEG"])
                
            with display_col:
                # --- HEAVY IMAGE PROCESSING SHIELD ---
                try:
                    processed_image = original_image.copy()
                    
                    # Apply Canvas Resizing
                    if processed_image.size != (new_width, new_height):
                        processed_image = processed_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Apply Canvas Cropping
                    p_width, p_height = processed_image.size
                    c_left = min(crop_left, p_width // 2)
                    c_right = p_width - min(crop_right, p_width // 2)
                    c_top = min(crop_top, p_height // 2)
                    c_bottom = p_height - min(crop_bottom, p_height // 2)
                    
                    if c_left < c_right and c_top < c_bottom:
                        processed_image = processed_image.crop((c_left, c_top, c_right, c_bottom))
                    
                    # Apply Selected Image Filters
                    if selected_filter == "Black & White":
                        processed_image = ImageOps.grayscale(processed_image)
                    elif selected_filter == "Sepia Tone":
                        gray = ImageOps.grayscale(processed_image)
                        processed_image = ImageOps.colorize(gray, "#704214", "#C0B283")
                    elif selected_filter == "Gaussian Blur":
                        processed_image = processed_image.filter(ImageFilter.GaussianBlur(radius=5))
                    elif selected_filter == "Contour Sketch":
                        processed_image = processed_image.filter(ImageFilter.CONTOUR)
                    elif selected_filter == "Vibrant Saturation":
                        enhancer = ImageEnhance.Color(processed_image)
                        processed_image = enhancer.enhance(2.5)
                    elif selected_filter == "Retro Negative":
                        if processed_image.mode in ("RGBA", "P"):
                            processed_image = processed_image.convert("RGB")
                        processed_image = ImageOps.invert(processed_image)
                    elif selected_filter == "Emboss Art":
                        processed_image = processed_image.filter(ImageFilter.EMBOSS)
                        
                    # Calculate dynamic file size metrics
                    original_size_kb = get_image_bytes_size(original_image, "PNG")
                    processed_size_kb = get_image_bytes_size(processed_image, export_format, compression_quality)
                    
                    # Render Side-by-Side Canvas
                    col_orig, col_proc = st.columns(2)
                    with col_orig:
                        st.markdown("### 📸 Original Reference Canvas")
                        st.image(original_image, use_container_width=True)
                        st.caption(f"Dimensions: {width}x{height} px | Size estimate: ~{original_size_kb:.2f} KB")
                        
                    with col_proc:
                        st.markdown(f"### ✨ Processed Matrix ({selected_filter})")
                        st.image(processed_image, use_container_width=True)
                        st.caption(f"Dimensions: {processed_image.size[0]}x{processed_image.size[1]} px | Dynamic Processed Size: **{processed_size_kb:.2f} KB**")
                    
                    # Compile the Download Engine Action Block
                    out_buffer = io.BytesIO()
                    if export_format == "JPEG":
                        if processed_image.mode in ("RGBA", "P"):
                            processed_image = processed_image.convert("RGB")
                        processed_image.save(out_buffer, format="JPEG", quality=compression_quality)
                        mime_type = "image/jpeg"
                        file_ext = "jpg"
                    else:
                        processed_image.save(out_buffer, format="PNG")
                        mime_type = "image/png"
                        file_ext = "png"
                        
                    st.markdown("---")
                    st.download_button(
                        label=f"📥 Download Output Asset ({export_format})",
                        data=out_buffer.getvalue(),
                        file_name=f"studio_export.{file_ext}",
                        mime=mime_type,
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"⚠️ Convolution Shield Exception Triggered: Failed to render transformations safely. Details: {e}")
                    
        except Exception as upload_err:
            st.error(f"💥 Faulty Input Stream: Unable to parse binary image file header logic. {upload_err}")
    else:
        st.info("💡 Standby: Please upload a photo file from your device to activate the image canvas filters.")

# ==========================================
# MODE B: UNIVERSAL QR ENGINE
# ==========================================
elif workspace_mode == "🔮 Universal QR Engine":
    st.title("🔮 Universal QR Engine")
    st.write("Generate dynamic structural QR payloads with deep canvas styling overrides.")
    
    # Global Style Parameters
    st.sidebar.subheader("🎨 Matrix Styling Overrides")
    dark_color = st.sidebar.color_picker("Line Data Element Color (Dark)", "#000000")
    light_color = st.sidebar.color_picker("Background Canvas Color (Light)", "#FFFFFF")
    scale_factor = st.sidebar.slider("Matrix Scale Resolution Factor", 1, 20, 10)
    
    # Pipeline Switcher Layout Tabs
    tab_text, tab_link, tab_image = st.tabs([
        "📝 Text to QR Pipeline", 
        "🔗 Link to QR Pipeline", 
        "🖼️ Image to QR Pipeline (Convert Image to QR)"
    ])
    
    qr_payload = None
    payload_valid = False
    
    # 1. Text to QR Pipeline
    with tab_text:
        st.markdown("### Plain-Text Literal Encoding Matrix")
        raw_text = st.text_area("Enter Literal Structural Content Paragraphs:", value="", placeholder="Enter content here...")
        if raw_text.strip():
            qr_payload = raw_text
            payload_valid = True
            st.success("✅ Plain text payload buffer verified.")
            
    # 2. Link to QR Pipeline
    with tab_link:
        st.markdown("### Native URI Link Architecture Redirect")
        target_url = st.text_input("Absolute Destination URL Paths:", value="", placeholder="https://example.com")
        if target_url.strip():
            if target_url.startswith(("http://", "https://")):
                qr_payload = target_url
                payload_valid = True
                st.success("✅ Target absolute web location structure locked.")
            else:
                st.warning("⚠️ Absolute URI targets require explicit structural protocols ('http://' or 'https://').")
                
    # 3. Image to QR Pipeline
    with tab_image:
        st.markdown("### Binary Object to Data URI Encoded Matrix")
        st.caption("Compresses small target imagery into Base64 strings to build high-capacity local QR arrays.")
        qr_image_file = st.file_uploader("Upload QR Target File asset...", type=["png", "jpg", "jpeg"], key="qr_img_upload")
        
        if qr_image_file is not None:
            try:
                # Open up object payload mapping 
                bin_img = Image.open(qr_image_file)
                # Auto-downscale to prevent massive data overhead errors in QR matrix sizes
                bin_img.thumbnail((80, 80))
                
                img_buf = io.BytesIO()
                bin_img.save(img_buf, format="PNG")
                b64_string = base64.b64encode(img_buf.getvalue()).decode("utf-8")
                
                # Compose explicit standard data URI block
                data_uri_payload = f"data:image/png;base64,{b64_string}"
                
                # Verify payload size restrictions
                if len(data_uri_payload) > 2953:
                    st.warning(f"⚠️ High Density Warning: Compressed payload contains {len(data_uri_payload)} characters. Scanners may struggle parsing symbols over 2,953 characters.")
                
                qr_payload = data_uri_payload
                payload_valid = True
                st.info(f"🧬 Data Block Segment Sample: `{data_uri_payload[:60]}...`")
            except Exception as b64_err:
                st.error(f"⚠️ Matrix Shield Exception Triggered: Failed to encode asset binaries. {b64_err}")

    # --- QR GENERATION & EXPORT ENGINE ---
    if payload_valid and qr_payload:
        st.markdown("---")
        st.subheader("🔮 Matrix Rendering Output Viewports")
        
        # Guarded Generation Execution Matrix
        try:
            # Build QR matrix with automatic error correction scaling
            qr_matrix = segno.make(qr_payload, error='M')
            
            # Export to system image byte payload layout
            qr_out_buf = io.BytesIO()
            qr_matrix.save(
                qr_out_buf, 
                kind='png', 
                scale=scale_factor, 
                dark=dark_color, 
                light=light_color
            )
            
            col_preview, col_metrics = st.columns([1, 1])
            with col_preview:
                st.image(qr_out_buf.getvalue(), caption="Compiled Dynamic QR Target Visual", use_container_width=False)
                
            with col_metrics:
                st.markdown("### 📊 Compiled Target Metrics")
                st.metric("Payload Length (Characters)", len(qr_payload))
                st.metric("QR Design Version String", f"Version {qr_matrix.version if hasattr(qr_matrix, 'version') else 'Auto'}")
                
                st.download_button(
                    label="📥 Download Compiled QR Image File",
                    data=qr_out_buf.getvalue(),
                    file_name="qr_studio_compiled.png",
                    mime="image/png",
                    use_container_width=True
                )
        except Exception as qr_gen_err:
            st.error(f"💥 Core Engine Intercept: Matrix creation pipeline aborted. Content string exceeds maximum alphanumeric QR payload allowances. Details: {qr_gen_err}")
    else:
        st.markdown("---")
        st.info("💡 Standby: Please configure data pipelines or upload binary streams above to write dynamic QR data.")
