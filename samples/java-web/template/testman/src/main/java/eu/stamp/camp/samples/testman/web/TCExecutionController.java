package eu.stamp.camp.samples.testman.web;
import eu.stamp.camp.samples.testman.domain.TCExecution;
import org.springframework.roo.addon.web.mvc.controller.scaffold.RooWebScaffold;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@RequestMapping("/tcexecutions")
@Controller
@RooWebScaffold(path = "tcexecutions", formBackingObject = TCExecution.class)
public class TCExecutionController {
}
