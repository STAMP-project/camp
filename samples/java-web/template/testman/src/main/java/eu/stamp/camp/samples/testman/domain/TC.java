package eu.stamp.camp.samples.testman.domain;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.tostring.RooToString;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.util.HashSet;
import java.util.Set;
import javax.persistence.CascadeType;
import javax.persistence.ManyToMany;

@RooJavaBean
@RooToString
@RooJpaActiveRecord
public class TC {

    /**
     */
    @NotNull
    @Size(min = 2)
    private String tcId;

    /**
     */
    @NotNull
    private String summary;

    /**
     */
    @NotNull
    private String steps;

    /**
     */
    @NotNull
    private String expectedResult;

    /**
     */
    @ManyToMany(cascade = CascadeType.ALL)
    private Set<TCExecution> executions = new HashSet<TCExecution>();
}
