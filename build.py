
# Импортируем pressets
import pressets

main_box = pressets.HtmlObj("box",
                            position = "absolute",
                            width = "1000px",
                            height = "700px",
                            top = "0px",
                            left = "0px",
                            padding = "20px",
                            background_color = "#f8f9fa",
                            border = "2px solid #dee2e6",
                            border_radius = "15px",
                            box_shadow = "0 4px 8px rgba(0, 0, 0, 0.1)"
                            )

box = pressets.HtmlObj("box",
                            position = "absolute",
                            width = "400px",
                            height = "400px",
                            top = "150px",
                            left = "600px",
                            padding = "20px",
                            background_color = "#f8f9fa",
                            border = "2px solid #dee2e6",
                            border_radius = "15px",
                            box_shadow = "0 4px 8px rgba(0, 0, 0, 0.1)"
                            )

main_box.add_obj(box)

index = pressets.html_file("index.html")

index.add_html_obj(main_box)
index.build_html()
index.load()