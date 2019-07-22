package eu.stamp.camp.samples.testman.web;
import eu.stamp.camp.samples.testman.domain.TC;
import org.springframework.roo.addon.web.mvc.controller.scaffold.RooWebScaffold;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@RequestMapping("/tcs")
@Controller
@RooWebScaffold(path = "tcs", formBackingObject = TC.class)
public class TCController {
}
